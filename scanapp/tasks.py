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
