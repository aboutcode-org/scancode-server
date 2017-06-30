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
def apply_scan_async(path, scan_id):
    scan_result = subprocess.check_output(['scancode', path])
    json_data = json.loads(scan_result)
    json_data = json.dumps(json_data)

    celery_scan = CeleryScan.objects.get(scan_id=scan_id)
    celery_scan.scan_results = str(json_data)
    celery_scan.is_complete = True
    celery_scan.save()
