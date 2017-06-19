import scancode
import json
import subprocess

class ScanCode(object):
    def __init__(self):
        pass

    def apply_scan(self, path):
        scan_result = subprocess.check_output(['scancode', path])
        json_data = json.loads(scan_result)
        return json_data
