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
import os
import subprocess
from datetime import datetime
from os.path import expanduser
from urlparse import urlparse

import git
import requests

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


@app.task
def scan_code_async(url, scan_id, path, file_name):
    """
    Create and save a file at `path` present at `url` using `scan_id` and bare `path` and
    `file_name` and apply the scan.
    """
    r = requests.get(url)
    path = path + file_name

    if r.status_code == 200:
        output_file = open(path, 'w')
        output_file.write(r.text.encode('utf-8'))
        apply_scan_async.delay(path, scan_id)


@app.task
def scan_code_async_final(url, scan_id):
    """
    Create and save a file at `path` present at `URL` using `scan_id` and bare `path`
    and apply the scan.
    """
    logger = logging.getLogger(__name__)
    logger.info('git repo detected')

    clean_url = ''.join(e for e in url if e.isalnum())

    dir_name = clean_url

    home_path = expanduser("~")

    os.chdir(home_path)

    os.mkdir(dir_name)

    repo = git.Repo.init(dir_name)
    origin = repo.create_remote('origin', url)
    origin.fetch()
    origin.pull(origin.refs[0].remote_head)

    logger.info('Done ! Remote repository cloned')

    filename = home_path + '/' + clean_url + '/'

    path = filename

    apply_scan_async.delay(path, scan_id)


@app.task
def apply_scan_async(path, scan_id):
    """
    Run a scancode scan on the files at `path` for `scan_id`
    and save results in the database.
    """
    # FIXME improve error checking when calling scan in subprocess.
    scan_result = subprocess.check_output(['scancode', path])
    json_data = json.loads(scan_result)
    save_results_to_db.delay(scan_id, json_data)


@app.task
def save_results_to_db(scan_id, json_data):
    """
    Fill database using `json_data` for given `scan_id`
    and add `end_scan_time` to true.
    """
    scan = Scan.objects.get(pk=scan_id)
    scan = fill_unfilled_scan_model(
        scan=scan,
        files_count=json_data['files_count'],
        scancode_notice=json_data['scancode_notice'],
        scancode_version=json_data['scancode_version'],
    )

    # logic to calculate total_error
    #    total_errors = 0
    #    for a_file in json_data['files']:
    #        for error in a_file['scan_errors']:
    #            total_errors = total_errors + 1

    for a_file in json_data['files']:
        scanned_file = ScannedFile(
            scan=scan,
            path=a_file['path']
        )
        scanned_file.save()

        for a_license in a_file['licenses']:
            license = License(
                scanned_file=scanned_file,
                key=a_license['key'],
                score=a_license['score'],
                short_name=a_license['short_name'],
                category=a_license['category'],
                owner=a_license['owner'],
                homepage_url=a_license['homepage_url'],
                text_url=a_license['text_url'],
                dejacode_url=a_license['dejacode_url'],
                spdx_license_key=a_license['spdx_license_key'],
                spdx_url=a_license['spdx_url'],
                start_line=a_license['start_line'],
                end_line=a_license['end_line'],
                matched_rule=a_license['matched_rule']
            )
            license.save()

        for a_copyright in a_file['copyrights']:
            copyright = Copyright(
                scanned_file=scanned_file,
                start_line=a_copyright['start_line'],
                end_line=a_copyright['end_line']
            )
            copyright.save()

            for copyright_holder in a_copyright['holders']:
                copyright_holder = CopyrightHolder(
                    copyright=copyright,
                    holder=copyright_holder
                )
                copyright_holder.save()

            for copyright_statement in a_copyright['statements']:
                copyright_statement = CopyrightStatement(
                    copyright=copyright,
                    statement=copyright_statement
                )
                copyright_statement.save()

            for copyright_author in a_copyright['authors']:
                copyright_author = CopyrightAuthor(
                    copyright=copyright,
                    author=copyright_author
                )
                copyright_author.save()

        for a_package in a_file['packages']:
            package = Package(
                scanned_file=scanned_file,
                package=a_package
            )
            package.save()

        for a_scan_error in a_file['scan_errors']:
            scan_error = ScanError(
                scanned_file=scanned_file,
                scan_error=a_scan_error
            )
            scan_error.save()

    scan.scan_end_time = datetime.now()
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


def parse_url(URL):
    """
        Parses the URL and checks if it's a git URL. If it is a git URL then the flag is set to 1.
    """
    flag = 0
    allowed_exts = ('git')
    url = urlparse(URL)
    if url.path.rsplit('.', 1)[1] in allowed_exts:
        flag = 1
    return flag
