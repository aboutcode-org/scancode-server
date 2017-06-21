from __future__ import absolute_import, unicode_literals

import json
import os
import subprocess

import requests


class ScanCode(object):
    def __init__(self):
        pass

    def apply_scan(self, path):
        scan_result = subprocess.check_output(['scancode', path])
        json_data = json.loads(scan_result)
        json_data = json.dumps(json_data)
        return json_data

    def get_content(self, URL):
        # list to store all the file names in the directory
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

            return self.apply_scan(path)

        else:
            return 'Some error has occured'
