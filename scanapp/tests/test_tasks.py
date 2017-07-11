from django.test import TestCase
from django.core.files import File
import json

from scanapp.tasks import scan_code_async
from scanapp.tasks import apply_scan_async
from scanapp.tasks import save_results_to_db
from scanapp.tasks import InsertIntoDB

from scanapp.models import ScanInfo
from scanapp.models import URLScanInfo
from scanapp.models import CodeInfo
from scanapp.models import ScanResult
from scanapp.models import ScanFileInfo
from scanapp.models import License
from scanapp.models import MatchedRule
from scanapp.models import MatchedRuleLicenses

class SaveResultsToDBTestCase(TestCase):
    def test_correct_save_result_to_db_with_scan_type_url(self):
        # TODO function not complete add more stuff to scanapp/tests/sample_json.txt
        # to test more
        URL='https://github.com/'
        insert_into_db = InsertIntoDB()
        scan_id = insert_into_db.create_scan_id(scan_type='URL')
        folder_name = None
        scan_type = 'URL'
        json_file = File(open('scanapp/tests/sample_json.txt', 'r'))
        for text in json_file:
            json_data = text
        
        json_data = json.loads(json_data)
        save_results_to_db(scan_id, json_data, scan_type, URL, folder_name)
        # assert statements tests each database
        scan_info = ScanInfo.objects.get(pk=scan_id)
        
        code_info = CodeInfo.objects.get(scan_info=scan_info)
        self.assertEqual(json_data['files_count'], code_info.total_code_files)
        
        url_scan_info = URLScanInfo.objects.get(scan_info=scan_info)
        self.assertEqual('https://github.com/', url_scan_info.URL)
        
        scan_result = ScanResult.objects.get(code_info=code_info)
        self.assertEqual(json_data, scan_result.scanned_json_result)
        
        scan_file_info = ScanFileInfo.objects.get(scan_result=scan_result)
        self.assertEqual(json_data['files'][0]['path'], scan_file_info.file_path)

        license = License.objects.get(scan_file_info=scan_file_info)
        self.assertEqual(json_data['files'][0]['licenses'][0]['key'], license.key)

        matched_rule = MatchedRule.objects.get(license=license)
        self.assertEqual(json_data['files'][0]['licenses'][0]['matched_rule']['identifier'], matched_rule.identifier)

        matched_rule_license = MatchedRuleLicenses.objects.get(license=license)
        self.assertEqual(json_data['files'][0]['licenses'][0]['matched_rule']['licenses'][0], matched_rule_license.license)

