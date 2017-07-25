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
import os
import subprocess
import requests
from datetime import datetime

from scanapp.models import Scan
from scanapp.models import ScannedFile
from scanapp.models import License
from scanapp.models import Copyright
from scanapp.models import CopyrightHolder
from scanapp.models import CopyrightStatement
from scanapp.models import CopyrightAuthor
from scanapp.models import Package
from scanapp.models import ScanError

from scanapp.celery import app

@app.task
def scan_code_async(URL, scan_id, path):
    """
    Create and save a file at `path` present at `URL` using `scan_id` and bare `path`
    and apply the scan.
    """
    scan_type = 'URL'

    # logic to check how many files are already present for the scan
    dir_list = list()
    dir_list = os.listdir(path)

    file_name = ''
    if len(dir_list) == 0:
        file_name = '1'
    else:
        dir_list.sort()
        file_name = str(1 + int(dir_list[-1]))

    r = requests.get(URL)
    path = path + file_name

    if r.status_code == 200:
        output_file = open(path, 'w')
        output_file.write(r.text.encode('utf-8'))
        folder_name = None
        apply_scan_async.delay(path, scan_id, scan_type, URL, folder_name)

@app.task
def apply_scan_async(path, scan_id):
    """
    Run a scancode scan on the files at `path` for `scan_id`, `scan_type`, `URL`, `folder_name`
    and save results in the database.
    """
    # FIXME improve error checking when calling scan in subprocess.
    scan_result = subprocess.check_output(['scancode', path])
    json_data = json.loads(scan_result)
    save_results_to_db.delay(scan_id, json_data)

@app.task
def save_results_to_db(scan_id, json_data):
    """
    Fill database using `json_data`, `scan_type`, `URL`, `folder_name` for given `scan_id`
    and change `is_complete` to true.
    """
    insert_into_db = InsertIntoDB()
    scan = Scan.objects.get(pk=scan_id)
    scan = insert_into_db.fill_unfilled_scan_model(
        scan = scan,
        files_count = json_data['files_count'],
        scancode_notice = json_data['scancode_notice'],
        scancode_version = json_data['scancode_version'],
    )

# logic to calculate total_error
#    total_errors = 0
#    for a_file in json_data['files']:
#        for error in a_file['scan_errors']:
#            total_errors = total_errors + 1

    for a_file in json_data['files']:
        scanned_file = insert_into_db.insert_into_scanned_file(
            scan = scan,
            path = a_file['path']
        )

        for a_license in a_file['licenses']:
            license = insert_into_db.insert_into_license(
                scanned_file = scanned_file,
                key = a_license['key'],
                score = a_license['score'],
                short_name = a_license['short_name'],
                category = a_license['category'],
                owner = a_license['owner'],
                homepage_url = a_license['homepage_url'],
                text_url = a_license['text_url'],
                dejacode_url = a_license['dejacode_url'],
                spdx_license_key = a_license['spdx_license_key'],
                spdx_url = a_license['spdx_url'],
                start_line = a_license['start_line'],
                end_line = a_license['end_line'],
                matched_rule = a_license['matched_rule']
            )

        for a_copyright in a_file['copyrights']:
            copyright = insert_into_db.insert_into_copyright(
                scanned_file = scanned_file,
                start_line = a_copyright['start_line'],
                end_line = a_copyright['end_line']
            )

            for copyright_holder in a_copyright['holders']:
                insert_into_db.insert_into_copyright_holders(
                    copyright = copyright,
                    holder = copyright_holder
                )

            for copyright_statement in a_copyright['statements']:
                insert_into_db.insert_into_copyright_statements(
                    copyright = copyright,
                    statement = copyright_statement
                )

            for copyright_author in a_copyright['authors']:
                insert_into_db.insert_into_copyright_author(
                    copyright = copyright,
                    author = copyright_author
                )

        for a_package in a_file['packages']:
            insert_into_db.insert_into_package(
                scanned_file = scanned_file,
                package = a_package
            )

        for a_scan_error in a_file['scan_errors']:
            insert_into_db.insert_into_scan_error(
                scanned_file = scanned_file,
                scan_error = a_scan_error
            )

    scan.scan_end_time = datetime.now()
    scan.save()

class InsertIntoDB(object):
    def __init__(self):
        pass

    def create_scan_id(self, user, url, scan_directory, scan_start_time):
        """
        Create the `scan_id` for an applied scan using `scan_type`
        and returns the `scan_id`.
        """
        scan = Scan(user=user, url=url, scan_directory=scan_directory, scan_start_time=scan_start_time)
        scan.save()
        scan_id = scan.id
        return scan_id

    def fill_unfilled_scan_model(self, scan, files_count, scancode_notice, scancode_version):
        """
        Fill the rest of the `Scan` model
        Half of the model is filled by `create_scan_id` method
        """
        scan.files_count = files_count
        scan.scancode_notice = scancode_notice
        scan.scancode_version = scancode_version
        scan.save()
        return scan

    def insert_into_scanned_file(self, scan, path):
        """
        Add `file_path into `ScannedFile` using `scan_result`
        and return `scanned_file`.
        """
        try:
            scanned_file = ScannedFile(
                scan = scan,
                path = path
            )
            scanned_file.save()
            return scanned_file

        except:
            print 'Database error at ScannedFile'

    def insert_into_license(self, scanned_file, key, score, short_name, category, owner, homepage_url, text_url, dejacode_url, spdx_license_key, spdx_url, start_line, end_line, matched_rule):
        """
        Add `category`, `start_line`, `spdx_url`, `text_url`, `spdx_license_key`, `homepage_url`, `score`, `end_line`, `key`, `owner`, `dejacode_url` into `License` model using `scanned_file`
        and return `license`.
        """
        try:
            license = License(
                scanned_file = scanned_file,
                key = key,
                score = score,
                short_name = short_name,
                category = category,
                owner = owner,
                homepage_url = homepage_url,
                text_url = text_url,
                dejacode_url = dejacode_url,
                spdx_license_key = spdx_license_key,
                spdx_url = spdx_url,
                start_line = start_line,
                end_line = end_line,
                matched_rule = matched_rule
            )
            license.save()
            return license

        except:
            print('Database error at model License')

    def insert_into_copyright(self, scanned_file, start_line, end_line):
        """
        Add `start_line`, `end_line` into model `Copyright` using `scanned_file`
        and return `copyright`
        """
        try:
            copyright = Copyright(
                scanned_file = scanned_file,
                start_line = start_line,
                end_line = end_line
            )
            copyright.save()
            return copyright

        except:
            print('Database error at model Copyright')

    def insert_into_copyright_holder(self, copyright, holder):
        """
        Add copyright `holder` into model `CopyrightHolder` using `copyright`
        """
        try:
            copyright_holder = CopyrightHolder(
                copyright = copyright,
                holder = holder
            )
            copyright_holder.save()

        except:
            print('Database error at model CopyrightHolder')

    def insert_into_copyright_statement(self, copyright, statement):
        """
        Add copyright `statement` into model `CopyrightStatement` using `copyright`
        """
        try:
            copyright_statement = CopyrightStatement(
                copyright = copyright,
                statement = statement
            )
            copyright_statement.save()

        except:
            print('Database error at model CopyrightStatement')

    def insert_into_copyright_author(self, copyright, author):
        """
        Add copyright `author` into model `CopyrightAuthor` using `copyright`
        """
        try:
            copyright_author = CopyrightAuthor(
                copyright = copyright,
                author = author
            )
            copyright_author.save()

        except:
            print('Database error at model CopyrightAuthor')

    def insert_into_Package(self, scanned_file, package):
        """
        Add `package` into model `Package` using `scanned_file`
        """
        try:
            package = Package(
                scanned_file = scanned_file,
                package = package
            )
            package.save()

        except:
            print 'Database error at model Package'

    def insert_into_scan_error(self, scanned_file, scan_error):
        """
        Add `scan_error` into model `ScanError` using `scanned_file`
        """
        try:
            scan_error = ScanError(
                scanned_file = scanned_file,
                scan_error = scan_error
            )
            scan_error.save()

        except:
            print 'Database error at model ScanError'
