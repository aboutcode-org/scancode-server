#
# Copyright (c) 2017 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-server/
# The scancode-server software is licensed under the Apache License version 2.0.
# Data generated with scancode-server require an acknowledgment.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with scancode-server or any scancode-server
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with scancode-server and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  scancode-server should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  scancode-server is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-server/ for support and download.

from __future__ import absolute_import, unicode_literals

import json
import logging
import subprocess

import requests
from django.utils import timezone

from scanapp.celery import app
from scanapp.models import Copyright
from scanapp.models import CopyrightAuthor
from scanapp.models import CopyrightHolder
from scanapp.models import CopyrightStatement
from scanapp.models import License
from scanapp.models import Package
from scanapp.models import Scan
from scanapp.models import ScanError
from scanapp.models import ScannedFile

logger = logging.getLogger(__name__)


@app.task
def scan_code_async(url, scan_id, path, file_name):
    """
    Create and save a file at `path` present at `url` using `scan_id`, bare `path`, `file_name`
    and apply the scan.
    """
    r = requests.get(url)
    path = path + file_name

    if r.status_code == 200:
        output_file = open(path, 'w')
        output_file.write(r.text.encode('utf-8'))
        apply_scan_async.delay(path, scan_id)


@app.task
def handle_special_urls(url, scan_id, path, host):
    """
    Create and initialise the git repository at a certain path and clone the git repo using `url`
    and then get the scan done.
    """
    if host == 'github.com':
        logger.info('git repo detected and cloned from the host github.com')
        subprocess.call(['git', 'clone', url, path])
        logger.info('Done ! Remote repository cloned')
        apply_scan_async(path, scan_id)


@app.task
def apply_scan_async(path, scan_id):
    """
    Run a scancode scan on the files at `path` for `scan_id`
    and save results in the database.
    """
    # FIXME improve error checking when calling scan in subprocess.
    scan_result = subprocess.check_output(['scancode', path])
    json_data = json.loads(scan_result)
    save_results_to_db.delay(scan_id, json_data, path)


@app.task
def save_results_to_db(scan_id, json_data, path):
    """
    Fill database using `json_data` for given `scan_id`
    and call `fill_rest_scanned_file_model` with the `path`
    """
    scan = Scan.objects.get(pk=scan_id)
    scan = fill_unfilled_scan_model(
        scan=scan,
        files_count=json_data['files_count'],
        scancode_notice=json_data['scancode_notice'],
        scancode_version=json_data['scancode_version'],
    )

    for scan_file in json_data['files']:
        scanned_file = ScannedFile(
            scan=scan,
            path=scan_file['path']
        )
        scanned_file.save()

        for scanned_license in scan_file['licenses']:
            license = License(
                scanned_file=scanned_file,
                key=scanned_license['key'],
                score=scanned_license['score'],
                short_name=scanned_license['short_name'],
                category=scanned_license['category'],
                owner=scanned_license['owner'],
                homepage_url=scanned_license['homepage_url'],
                text_url=scanned_license['text_url'],
                dejacode_url=scanned_license['dejacode_url'],
                spdx_license_key=scanned_license['spdx_license_key'],
                spdx_url=scanned_license['spdx_url'],
                start_line=scanned_license['start_line'],
                end_line=scanned_license['end_line'],
                matched_rule=scanned_license['matched_rule']
            )
            license.save()

        for scanned_copyright in scan_file['copyrights']:
            copyright = Copyright(
                scanned_file=scanned_file,
                start_line=scanned_copyright['start_line'],
                end_line=scanned_copyright['end_line']
            )
            copyright.save()

            for scan_copyright_holder in scanned_copyright['holders']:
                copyright_holder = CopyrightHolder(
                    copyright=copyright,
                    holder=scan_copyright_holder
                )
                copyright_holder.save()

            for scan_copyright_statement in scanned_copyright['statements']:
                copyright_statement = CopyrightStatement(
                    copyright=copyright,
                    statement=scan_copyright_statement
                )
                copyright_statement.save()

            for scan_copyright_author in scanned_copyright['authors']:
                copyright_author = CopyrightAuthor(
                    copyright=copyright,
                    author=scan_copyright_author
                )
                copyright_author.save()

        for scan_package in scan_file['packages']:
            package = Package(
                scanned_file=scanned_file,
                package=scan_package
            )
            package.save()

        for scanned_scan_error in scan_file['scan_errors']:
            scan_error = ScanError(
                scanned_file=scanned_file,
                scan_error=scanned_scan_error
            )
            scan_error.save()

    fill_rest_scanned_file_model.delay(path, scan_id)


@app.task
def fill_rest_scanned_file_model(path, scan_id):
    """
    Fill the rest ScannedFile model by using another subprocess call
    """
    scanned_file_results = subprocess.check_output(['scancode', '--info', '-f', 'json-pp', path])
    json_scanned_file_results = json.loads(scanned_file_results)
    for file in json_scanned_file_results['files']:
        scanned_file = ScannedFile.objects.get(path=file['path'])
        scanned_file.type = file['type']
        scanned_file.name = file['name']
        scanned_file.base_name = file['base_name']
        scanned_file.extension = file['extension']
        scanned_file.date = file['date']
        scanned_file.size = file['size']
        scanned_file.sha1 = file['sha1']
        scanned_file.md5 = file['md5']
        scanned_file.files_count = file['files_count']
        scanned_file.mime_type = file['mime_type']
        scanned_file.file_type = file['file_type']
        scanned_file.programming_language = file['programming_language']
        scanned_file.is_binary = file['is_binary']
        scanned_file.is_text = file['is_text']
        scanned_file.is_archive = file['is_archive']
        scanned_file.is_media = file['is_media']
        scanned_file.is_source = file['is_source']
        scanned_file.is_script = file['is_script']
        scanned_file.save()
    scan = Scan.objects.get(pk=scan_id)
    scan.scan_end_time = timezone.now()
    scan.save()


def create_scan_id(user, url, scan_directory, scan_start_time):
    """
    Create the `scan_id` for an applied scan using `user`, `url`, `scan_directory` and
    `scan_start_time`
    and returns the `scan_id`.
    """
    scan = Scan(
        user=user,
        url=url,
        scan_directory=scan_directory,
        scan_start_time=scan_start_time
    )
    scan.save()
    scan_id = scan.id
    return scan_id


def fill_unfilled_scan_model(scan, files_count, scancode_notice, scancode_version):
    """
    Fill the rest of the `Scan` model
    Half of the model is filled by `create_scan_id` method
    """
    scan.files_count = files_count
    scan.scancode_notice = scancode_notice
    scan.scancode_version = scancode_version
    scan.save()
    return scan
