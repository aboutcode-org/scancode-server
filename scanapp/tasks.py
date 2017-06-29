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

from scanapp.models import CeleryScan
from scanapp.models import ScanInfo
from scanapp.models import UserInfo
from scanapp.models import URLScanInfo
from scanapp.models import LocalScanInfo
from scanapp.models import CodeInfo
from scanapp.models import ScanResult
from scanapp.models import ScanFileInfo
from scanapp.models import License
from scanapp.models import MatchedRule
from scanapp.models import MatchedRuleLicenses
from scanapp.models import Copyright
from scanapp.models import CopyrightHolders
from scanapp.models import CopyrightStatements
from scanapp.models import CopyrightAuthor
from scanapp.models import Package
from scanapp.models import ScanError

from scanapp.celery import app

@app.task
def scan_code_async(URL, scan_id):
    dir_list = list()
    dir_list = os.listdir('media/URL/')

    # name of file where the content will be stored
    file_name = ''
    if len(dir_list) == 0:
        file_name = '1'
    else:
        dir_list.sort()
        file_name = str(1 + int(dir_list[-1]))

    # send the request to get the URL
    r = requests.get(URL)
    path = 'media/URL/' + file_name

    if r.status_code == 200:
        # open the file in write mode
        output_file = open(path, 'w')

        # write the content into the file
        # This doesn't works without encoding part
        output_file.write(r.text.encode('utf-8'))

        # pass the path to apply_scan function

        return apply_scan_async.delay(path, scan_id)

    else:
        return 'Some error has occured'

@app.task
def apply_scan_async(path, scan_id, *args, **kwargs):
    """
    Output: scanned data in JSON format
    Input: path, scan_id
    call another function: save_results_to_db with the output
    """
    # apply scan to the recieved data
    scan_result = subprocess.check_output(['scancode', path])

    # load the data as json output
    json_data = json.loads(scan_result)

    #call the save_results_to_db function
    save_results_to_db.delay(scan_id=scan_id, json_data=json_data, scan_type=kwargs['scan_type'])

@app.task
def save_results_to_db(*args, **kwargs):
    json_data = kwargs['json_data']
    # Insert into db
    insert_into_db = InsertIntoDB()
    scan_id = kwargs['scan_id']
    code_info = insert_into_db.insert_code_info(
        scan_id,
        scan_info = ScanInfo.objects.get(pk=scan_id),
        total_code_files = json_data['files_count'],
        code_size = 4096,
        scan_type=kwargs['scan_type'],
        # TODO correct this
        folder_name = 'something/',
    )

    # calculate total scan errors
    total_errors = 0
    for a_file in json_data['files']:
        for error in a_file['scan_errors']:
            total_errors = total_errors + 1

    scan_result = insert_into_db.save_results(
        code_info = code_info,
        scanned_json_result = json_data,
        scanned_html_result = '<h4>' + str(json.dumps(json_data)) + '</h4>',
        scancode_notice = json_data['scancode_notice'],
        scancode_version = json_data['scancode_version'],
        files_count = json_data['files_count'],
        total_errors = total_errors,
        scan_time = 5000,
    )

    # create scan_file_info for every new file path that comes our way
    for a_file in json_data['files']:
        scan_file_info = insert_into_db.scan_file_info(
            scan_result = scan_result,
            file_path = a_file['path']
        )

        for a_license in a_file['licenses']:
            license = insert_into_db.add_license(
                scan_file_info = scan_file_info,
                category = a_license['category'],
                start_line = a_license['start_line'],
                spdx_url = a_license['spdx_url'],
                text_url = a_license['text_url'],
                spdx_license_key = a_license['spdx_license_key'],
                homepage_url = a_license['homepage_url'],
                score = a_license['score'],
                end_line = a_license['end_line'],
                key = a_license['key'],
                owner = a_license['owner'],
                dejacode_url = a_license['dejacode_url'],
            )

            a_matched_rule = a_license['matched_rule']
            matched_rule = insert_into_db.matched_rule(
                license = license,
                license_choice = a_matched_rule['license_choice'],
                identifier = a_matched_rule['identifier']
            )

            matched_rule_licenses = a_matched_rule['licenses']
            for a_matched_rule_license in matched_rule_licenses:
                insert_into_db.matched_rule_licenses(
                    matched_rule = matched_rule,
                    license = a_matched_rule_license
                )

        for a_copyright in a_file['copyrights']:
            copyright = insert_into_db.add_copyright(
                scan_file_info = scan_file_info,
                start_line = a_copyright['start_line'],
                end_line = a_copyright['end_line']
            )

            for copyright_holder in a_copyright['holders']:
                insert_into_db.copyright_holder(
                    copyright = copyright,
                    holder = copyright_holder
                )

            for copyright_statement in a_copyright['statements']:
                insert_into_db.copyright_statements(
                    copyright = copyright,
                    statement = copyright_statement
                )

            for copyright_author in a_copyright['authors']:
                insert_into_db.copyright_author(
                    copyright = copyright,
                    author = copyright_author
                )

        for a_package in a_file['packages']:
            insert_into_db.add_package(
                scan_file_info = scan_file_info,
                package = a_package
            )

        for a_scan_error in a_file['scan_errors']:
            insert_into_db.add_scan_error(
                scan_file_info = scan_file_info,
                scan_error = a_scan_error
            )

    # Finally change the is_complete variable to True
    scan_id = kwargs['scan_id']
    scan_info = ScanInfo.objects.get(pk=scan_id)
    scan_info.is_complete=True
    scan_info.save()

class InsertIntoDB(object):
    def __init__(self):
        pass

    def create_scan_id(self, *args, **kwargs):
        # take scan_type from the kwargs
        scan_type = kwargs['scan_type']

        # create an object of ScanInfo
        scan_info = ScanInfo(scan_type=scan_type, is_complete=False)

        # save the instance to the database
        scan_info.save()

        # get the scan_id from the instance
        scan_id = scan_info.id

        # return the scan_id
        return scan_id

    def insert_code_info(self, scan_id, *args, **kwargs):
        # get the scan_info using the scan_id
        scan_info = ScanInfo.objects.get(pk=scan_id)

        # Insert into CodeInfo table
        code_info = CodeInfo(
            scan_info = kwargs['scan_info'],
            total_code_files = kwargs['total_code_files'],
            code_size = kwargs['code_size']
        )
        code_info.save()

        # Insert into URLScanInfo or LocalScanInfo table
        if(kwargs['scan_type'] == 'URL'):
            URL_scan_info = URLScanInfo(scan_info=scan_info, URL=kwargs['URL'])
            URL_scan_info.save()

        elif(kwargs['scan_type'] == 'localscan'):
            local_scan_info = LocalScanInfo(scan_info=scan_info, folder_name=kwargs['folder_name'])
            local_scan_info.save()

        else:
            print "Error found. Check the kwargs"

        return code_info

    def save_results(self, *args, **kwargs):
        try:
            # put the stuff to ScanResult model
            scan_result = ScanResult(
                code_info = kwargs['code_info'],
                scanned_json_result = kwargs['scanned_json_result'],
                scanned_html_result = kwargs['scanned_html_result'],
                scancode_notice = kwargs['scancode_notice'],
                scancode_version = kwargs['scancode_version'],
                files_count = kwargs['files_count'],
                total_errors = kwargs['total_errors'],
                scan_time = kwargs['scan_time']
            )

            scan_result.save()

            return scan_result

        except:
            print 'Unable to put data into the database SaveResult'

    def scan_file_info(self, *args, **kwargs):
        try:
            scan_file_info = ScanFileInfo(
                scan_result = kwargs['scan_result'],
                file_path = kwargs['file_path']
            )

            scan_file_info.save()

            return scan_file_info

        except:
            print 'Database error at ScanFileInfo'

    def add_license(self, *args, **kwargs):
        try:
            license = License(
                scan_file_info = kwargs['scan_file_info'],
                category = kwargs['category'],
                start_line = kwargs['start_line'],
                spdx_url = kwargs['spdx_url'],
                text_url = kwargs['text_url'],
                spdx_license_key = kwargs['spdx_license_key'],
                homepage_url = kwargs['homepage_url'],
                score = kwargs['score'],
                end_line = kwargs['end_line'],
                key = kwargs['key'],
                owner = kwargs['owner'],
                dejacode_url = kwargs['dejacode_url']
            )

            license.save()

            return license

        except:
            print('Database error at model License')

    def matched_rule(self, *args, **kwargs):
        try:
            matched_rule = MatchedRule(
                license = kwargs['license'],
                license_choice = kwargs['license_choice'],
                identifier = kwargs['identifier']
            )

            matched_rule.save()

            return matched_rule

        except:
            print('Database error at model MatchedRule')

    def matched_rule_licenses(self, *args, **kwargs):
        try:
            matched_rule_licenses = MatchedRuleLicenses(
                matched_rule = kwargs['matched_rule'],
                license = kwargs['license']
            )

            matched_rule_licenses.save()

        except:
            print('Database error at model matchedRuleLicense')

    def add_copyright(self, *args, **kwargs):
        try:
            copyright = Copyright(
                scan_file_info = kwargs['scan_file_info'],
                start_line = kwargs['start_line'],
                end_line = kwargs['end_line']
            )

            copyright.save()

            return copyright

        except:
            print('Database error at model Copyright')

    def copyright_holder(self, *args, **kwargs):
        try:
            copyright_holder = CopyrightHolders(
                copyright = kwargs['copyright'],
                holder = kwargs['holder']
            )

            copyright_holder.save()

        except:
            print('Database error at model CopyrightHolder')

    def copyright_statements(self, *args, **kwargs):
        try:
            copyright_statements = CopyrightStatements(
                copyright = kwargs['copyright'],
                statement = kwargs['statement']
            )

            copyright_statements.save()

        except:
            print('Database error at model CopyrightStatements')

    def copyright_author(self, *args, **kwargs):
        try:
            copyright_author = CopyrightAuthor(
                copyright = kwargs['copyright'],
                author = kwargs['author']
            )

            copyright_author.save()

        except:
            print('Database error at model CopyrightAuthor')

    def add_Package(self, *args, **kwargs):
        try:
            package = Package(
                scan_file_info = kwargs['scan_file_info'],
                package = kwargs['package']
            )

            package.save()

        except:
            print 'Database error at model Package'

    def add_scan_error(self, *args, **kwargs):
        try:
            scan_error = ScanError(
                scan_file_info = kwargs['scan_file_info'],
                scan_error = kwargs['scan_error']
            )

            scan_error.save()

        except:
            print 'Database error at model ScanError'
