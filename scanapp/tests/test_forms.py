from django.test import TestCase
from django.core.files.uploadedfile import InMemoryUploadedFile
from scanapp.forms import URLScanForm
from scanapp.forms import LocalScanForm

class UrlScanFormTestCase(TestCase):
    def test_correct_url_scan_form(self):
        correct_form_data = {'URL': 'https://github.com'}
        correct_url_scan_form = URLScanForm(data=correct_form_data)
        self.assertTrue(correct_url_scan_form.is_valid())
        self.assertEqual('https://github.com', correct_url_scan_form.data['URL'])
    
    def test_wrong_url_scan_form(self):
        wrong_form_data = {'URL': 'not an URL'}
        wrong_url_scan_form = URLScanForm(data=wrong_form_data)
        self.assertFalse(wrong_url_scan_form.is_valid())    
    
    def test_empty_url_scan_form(self):
        empty_form_data = {'URL': ''}        
        empty_url_scan_form = URLScanForm(data=empty_form_data)  
        self.assertFalse(empty_url_scan_form.is_valid())

class LocalScanFormTestCase(TestCase):
    def test_local_scan_form(self):
        a_file = InMemoryUploadedFile('name', 'local', 'name.txt', 400, 'application/json', 'utf-8', 'no extra')
        correct_form_data = {'upload_from_local': a_file}
        wrong_form_data = {'upload_from_local': 'not a path'}
        empty_form_data = {'upload_from_local': ''}
        correct_local_scan_form = LocalScanForm(data=correct_form_data)
        wrong_local_scan_form = LocalScanForm(data=wrong_form_data)
        empty_local_scan_form = LocalScanForm(data=empty_form_data)
        self.assertEqual('name.txt', str(a_file))
        self.assertTrue(correct_local_scan_form.is_valid())
        self.assertEqual('/home/ranvir/Documents/file.txt', correct_local_scan_form.data['upload_from_local'])
        self.assertFalse(wrong_local_scan_form.is_valid())
        self.assertFalse(empty_local_scan_form.is_valid())


