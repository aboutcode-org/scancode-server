from django.test import TestCase

import json

from django.contrib.auth.models import User
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

class ScanInfoTestCase(TestCase):
    def test_scan_info_added(self):
        url_scan_info = ScanInfo.objects.create(scan_type='URL', is_complete=True)
        local_scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        url_scan_info_one = ScanInfo.objects.get(pk=url_scan_info.pk)
        local_scan_info_one = ScanInfo.objects.get(pk=local_scan_info.pk)
        self.assertTrue(url_scan_info_one.is_complete)
        self.assertFalse(local_scan_info_one.is_complete)
        self.assertEqual(url_scan_info.scan_type, str(url_scan_info))
        self.assertEqual('Scan Info', url_scan_info._meta.verbose_name_plural)

class UserInfoTestCase(TestCase):
    def test_user_info_added(self):
        user = User.objects.create(username='username', password='password')
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        user_info = UserInfo.objects.create(user=user, scan_info=scan_info)
        self.assertEqual('username', user_info.user.username)
        self.assertNotEqual('pass word', user_info.user.password)
        self.assertEqual(user_info.user.username, str(user_info))
        self.assertEqual('User Info', user_info._meta.verbose_name_plural) 

class URLScanInfoTestCase(TestCase):
    def test_url_scan_info_added(self):
        scan_info = ScanInfo.objects.create(scan_type='URL', is_complete=False)
        url_scan_info = URLScanInfo.objects.create(URL='https://github.com/nexb/scancode-server/', scan_info=scan_info)
        self.assertEqual('https://github.com/nexb/scancode-server/', url_scan_info.URL)
        self.assertEqual(url_scan_info.URL, str(url_scan_info))
        self.assertEqual('URL Scan Info', url_scan_info._meta.verbose_name_plural)

class LocalScanInfoTestCase(TestCase):
    def test_local_scan_info_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        local_scan_info = LocalScanInfo.objects.create(folder_name='/home/nexb/scancode/', scan_info=scan_info)
        self.assertEqual('/home/nexb/scancode/', local_scan_info.folder_name)
        self.assertEqual(local_scan_info.folder_name, str(local_scan_info))
        self.assertEqual('Local Scan Info', local_scan_info._meta.verbose_name_plural)

class CodeInfoTestCase(TestCase):
    def test_code_info_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        code_info = CodeInfo.objects.create(total_code_files=2000, code_size=4096, scan_info=scan_info)
        self.assertEqual(2000, code_info.total_code_files)
        self.assertEqual(4096, code_info.code_size)
        self.assertEqual(str(code_info.total_code_files), str(code_info))
        self.assertEqual('Code Info', code_info._meta.verbose_name_plural)

class ScanResultTestCase(TestCase):
    def test_scan_results_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        code_info = CodeInfo.objects.create(total_code_files=2000, code_size=4096, scan_info=scan_info)
        result = {'scanned_json_result': 'some result',
                  'scanned_html_result': '<h1>HTML result</h1>',
                  'scancode_notice': 'Some dummy notice',
                  'scancode_version': '2.0.0rc3',
                  'files_count': 200,
                  'total_errors': 0,
                  'scan_time': 5000}
        scan_result = ScanResult.objects.create(
            code_info = code_info,
            scanned_json_result = result['scanned_json_result'],
            scanned_html_result = result['scanned_html_result'],
            scancode_notice = result['scancode_notice'],
            scancode_version = result['scancode_version'],
            files_count = result['files_count'],
            total_errors = result['total_errors'],
            scan_time = result['scan_time']
        )
        self.assertEqual('2.0.0rc3', scan_result.scancode_version)
        self.assertEqual(str(scan_result.total_errors), str(scan_result))
        self.assertEqual('scan results', str(scan_result._meta.verbose_name_plural))

class ScanFileInfoTestCase(TestCase):
    def test_scan_file_info_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        code_info = CodeInfo.objects.create(total_code_files=2000, code_size=4096, scan_info=scan_info)
        result = {'scanned_json_result': 'some result',
                  'scanned_html_result': '<h1>HTML result</h1>',
                  'scancode_notice': 'Some dummy notice',
                  'scancode_version': '2.0.0rc3',
                  'files_count': 200,
                  'total_errors': 0,
                  'scan_time': 5000}
        scan_result = ScanResult.objects.create(
            code_info = code_info,
            scanned_json_result = result['scanned_json_result'],
            scanned_html_result = result['scanned_html_result'],
            scancode_notice = result['scancode_notice'],
            scancode_version = result['scancode_version'],
            files_count = result['files_count'],
            total_errors = result['total_errors'],
            scan_time = result['scan_time']
        )
        scan_file_info = ScanFileInfo.objects.create(scan_result=scan_result, file_path='/home/nexb/server/')
        self.assertEqual('/home/nexb/server/', scan_file_info.file_path)
        self.assertEqual(scan_file_info.file_path, str(scan_file_info))
        self.assertEqual('Scan File Info', str(scan_file_info._meta.verbose_name_plural))

class LicenseTestCase(TestCase):
    def test_license_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        code_info = CodeInfo.objects.create(total_code_files=2000, code_size=4096, scan_info=scan_info)
        result = {'scanned_json_result': 'some result',
                  'scanned_html_result': '<h1>HTML result</h1>',
                  'scancode_notice': 'Some dummy notice',
                  'scancode_version': '2.0.0rc3',
                  'files_count': 200,
                  'total_errors': 0,
                  'scan_time': 5000}
        scan_result = ScanResult.objects.create(
            code_info = code_info,
            scanned_json_result = result['scanned_json_result'],
            scanned_html_result = result['scanned_html_result'],
            scancode_notice = result['scancode_notice'],
            scancode_version = result['scancode_version'],
            files_count = result['files_count'],
            total_errors = result['total_errors'],
            scan_time = result['scan_time']
        )
        scan_file_info = ScanFileInfo.objects.create(scan_result=scan_result, file_path='/home/nexb/server/')
        license = License.objects.create(
            scan_file_info = scan_file_info, 
            category = 'some category',
            start_line = 21,
            spdx_url = 'https://github.com/',
            text_url = 'http://github.com/',
            spdx_license_key = 'mit', 
            homepage_url = 'https://github.com/',
            score = 78,
            end_line = 567,
            key = 'A',
            owner = 'mit',
            dejacode_url = 'https://github.com'
        )
        self.assertEqual('mit', license.owner)
        self.assertEqual(license.key, str(license))
        self.assertEqual('Licenses', license._meta.verbose_name_plural)

class MatchedRuleTestCase(TestCase):
    def test_matched_rule_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        code_info = CodeInfo.objects.create(total_code_files=2000, code_size=4096, scan_info=scan_info)
        result = {'scanned_json_result': 'some result',
                  'scanned_html_result': '<h1>HTML result</h1>',
                  'scancode_notice': 'Some dummy notice',
                  'scancode_version': '2.0.0rc3',
                  'files_count': 200,
                  'total_errors': 0,
                  'scan_time': 5000}
        scan_result = ScanResult.objects.create(
            code_info = code_info,
            scanned_json_result = result['scanned_json_result'],
            scanned_html_result = result['scanned_html_result'],
            scancode_notice = result['scancode_notice'],
            scancode_version = result['scancode_version'],
            files_count = result['files_count'],
            total_errors = result['total_errors'],
            scan_time = result['scan_time']
        )
        scan_file_info = ScanFileInfo.objects.create(scan_result=scan_result, file_path='/home/nexb/server/')
        license = License.objects.create(
            scan_file_info = scan_file_info, 
            category = 'some category',
            start_line = 21,
            spdx_url = 'https://github.com/',
            text_url = 'http://github.com/',
            spdx_license_key = 'mit', 
            homepage_url = 'https://github.com/',
            score = 78,
            end_line = 567,
            key = 'A',
            owner = 'mit',
            dejacode_url = 'https://github.com'
        )
        matched_rule = MatchedRule.objects.create(license=license, license_choice=False, identifier='mit')
        self.assertEqual('mit', matched_rule.identifier)
        self.assertEqual(str(matched_rule), str(matched_rule.license_choice))
        self.assertEqual('Matched Rule', matched_rule._meta.verbose_name_plural)

class MatchedRuleLicenseTestCase(TestCase):
    def test_matched_rule_license_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        code_info = CodeInfo.objects.create(total_code_files=2000, code_size=4096, scan_info=scan_info)
        result = {'scanned_json_result': 'some result',
                  'scanned_html_result': '<h1>HTML result</h1>',
                  'scancode_notice': 'Some dummy notice',
                  'scancode_version': '2.0.0rc3',
                  'files_count': 200,
                  'total_errors': 0,
                  'scan_time': 5000}
        scan_result = ScanResult.objects.create(
            code_info = code_info,
            scanned_json_result = result['scanned_json_result'],
            scanned_html_result = result['scanned_html_result'],
            scancode_notice = result['scancode_notice'],
            scancode_version = result['scancode_version'],
            files_count = result['files_count'],
            total_errors = result['total_errors'],
            scan_time = result['scan_time']
        )
        scan_file_info = ScanFileInfo.objects.create(scan_result=scan_result, file_path='/home/nexb/server/')
        license = License.objects.create(
            scan_file_info = scan_file_info, 
            category = 'some category',
            start_line = 21,
            spdx_url = 'https://github.com/',
            text_url = 'http://github.com/',
            spdx_license_key = 'mit', 
            homepage_url = 'https://github.com/',
            score = 78,
            end_line = 567,
            key = 'A',
            owner = 'mit',
            dejacode_url = 'https://github.com'
        )
        matched_rule = MatchedRule.objects.create(license=license, license_choice=False, identifier='mit')
        matched_rule_license = MatchedRuleLicenses(matched_rule=matched_rule, license='mit')
        self.assertEqual('mit', matched_rule_license.license)
        self.assertEqual(str(matched_rule_license), matched_rule_license.license)
        self.assertEqual('Matched Rule License', matched_rule_license._meta.verbose_name_plural)

class CopyrightTestCase(TestCase):
    def test_copyright_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        code_info = CodeInfo.objects.create(total_code_files=2000, code_size=4096, scan_info=scan_info)
        result = {'scanned_json_result': 'some result',
                  'scanned_html_result': '<h1>HTML result</h1>',
                  'scancode_notice': 'Some dummy notice',
                  'scancode_version': '2.0.0rc3',
                  'files_count': 200,
                  'total_errors': 0,
                  'scan_time': 5000}
        scan_result = ScanResult.objects.create(
            code_info = code_info,
            scanned_json_result = result['scanned_json_result'],
            scanned_html_result = result['scanned_html_result'],
            scancode_notice = result['scancode_notice'],
            scancode_version = result['scancode_version'],
            files_count = result['files_count'],
            total_errors = result['total_errors'],
            scan_time = result['scan_time']
        )
        scan_file_info = ScanFileInfo.objects.create(scan_result=scan_result, file_path='/home/nexb/server/')
        copyright = Copyright.objects.create(scan_file_info=scan_file_info, start_line=800, end_line=1000)
        self.assertEqual(1000, copyright.end_line)
        self.assertEqual(str(copyright.start_line), str(copyright))
        self.assertEqual('Copyrights', copyright._meta.verbose_name_plural)

class CopyrightHoldersTestCase(TestCase):
    def test_copyright_holders_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        code_info = CodeInfo.objects.create(total_code_files=2000, code_size=4096, scan_info=scan_info)
        result = {'scanned_json_result': 'some result',
                  'scanned_html_result': '<h1>HTML result</h1>',
                  'scancode_notice': 'Some dummy notice',
                  'scancode_version': '2.0.0rc3',
                  'files_count': 200,
                  'total_errors': 0,
                  'scan_time': 5000}
        scan_result = ScanResult.objects.create(
            code_info = code_info,
            scanned_json_result = result['scanned_json_result'],
            scanned_html_result = result['scanned_html_result'],
            scancode_notice = result['scancode_notice'],
            scancode_version = result['scancode_version'],
            files_count = result['files_count'],
            total_errors = result['total_errors'],
            scan_time = result['scan_time']
        )
        scan_file_info = ScanFileInfo.objects.create(scan_result=scan_result, file_path='/home/nexb/server/')
        copyright = Copyright.objects.create(scan_file_info=scan_file_info, start_line=800, end_line=1000)
        copyright_holders = CopyrightHolders.objects.create(copyright=copyright, holder='mit')
        self.assertEqual('mit', copyright_holders.holder)
        self.assertEqual(str(copyright_holders.holder), str(copyright_holders))
        self.assertEqual('Copyright Holders', copyright_holders._meta.verbose_name_plural)

class CopyrightStatementsTestCase(TestCase):
    def test_copyright_statements_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        code_info = CodeInfo.objects.create(total_code_files=2000, code_size=4096, scan_info=scan_info)
        result = {'scanned_json_result': 'some result',
                  'scanned_html_result': '<h1>HTML result</h1>',
                  'scancode_notice': 'Some dummy notice',
                  'scancode_version': '2.0.0rc3',
                  'files_count': 200,
                  'total_errors': 0,
                  'scan_time': 5000}
        scan_result = ScanResult.objects.create(
            code_info = code_info,
            scanned_json_result = result['scanned_json_result'],
            scanned_html_result = result['scanned_html_result'],
            scancode_notice = result['scancode_notice'],
            scancode_version = result['scancode_version'],
            files_count = result['files_count'],
            total_errors = result['total_errors'],
            scan_time = result['scan_time']
        )
        scan_file_info = ScanFileInfo.objects.create(scan_result=scan_result, file_path='/home/nexb/server/')
        copyright = Copyright.objects.create(scan_file_info=scan_file_info, start_line=800, end_line=1000)
        copyright_statement = CopyrightStatements.objects.create(copyright=copyright, statement='mit copyright statement')
        self.assertEqual('mit copyright statement', copyright_statement.statement)
        self.assertEqual(str(copyright_statement.statement), str(copyright_statement))
        self.assertEqual('Copyright Statements', copyright_statement._meta.verbose_name_plural)

class CopyrightAuthorsTestCase(TestCase):
    def test_copyright_authors_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        code_info = CodeInfo.objects.create(total_code_files=2000, code_size=4096, scan_info=scan_info)
        result = {'scanned_json_result': 'some result',
                  'scanned_html_result': '<h1>HTML result</h1>',
                  'scancode_notice': 'Some dummy notice',
                  'scancode_version': '2.0.0rc3',
                  'files_count': 200,
                  'total_errors': 0,
                  'scan_time': 5000}
        scan_result = ScanResult.objects.create(
            code_info = code_info,
            scanned_json_result = result['scanned_json_result'],
            scanned_html_result = result['scanned_html_result'],
            scancode_notice = result['scancode_notice'],
            scancode_version = result['scancode_version'],
            files_count = result['files_count'],
            total_errors = result['total_errors'],
            scan_time = result['scan_time']
        )
        scan_file_info = ScanFileInfo.objects.create(scan_result=scan_result, file_path='/home/nexb/server/')
        copyright = Copyright.objects.create(scan_file_info=scan_file_info, start_line=800, end_line=1000)
        copyright_author = CopyrightAuthor.objects.create(copyright=copyright, author='Ranvir Singh')
        self.assertEqual('Ranvir Singh', copyright_author.author)
        self.assertEqual(str(copyright_author.author), str(copyright_author))
        self.assertEqual('Copyright Authors', copyright_author._meta.verbose_name_plural)

class PackageTestCase(TestCase):
    def test_package_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        code_info = CodeInfo.objects.create(total_code_files=2000, code_size=4096, scan_info=scan_info)
        result = {'scanned_json_result': 'some result',
                  'scanned_html_result': '<h1>HTML result</h1>',
                  'scancode_notice': 'Some dummy notice',
                  'scancode_version': '2.0.0rc3',
                  'files_count': 200,
                  'total_errors': 0,
                  'scan_time': 5000}
        scan_result = ScanResult.objects.create(
            code_info = code_info,
            scanned_json_result = result['scanned_json_result'],
            scanned_html_result = result['scanned_html_result'],
            scancode_notice = result['scancode_notice'],
            scancode_version = result['scancode_version'],
            files_count = result['files_count'],
            total_errors = result['total_errors'],
            scan_time = result['scan_time']
        )
        scan_file_info = ScanFileInfo.objects.create(scan_result=scan_result, file_path='/home/nexb/server/')
        package = Package.objects.create(scan_file_info=scan_file_info, package='bootstrap')
        self.assertEqual('bootstrap', package.package)
        self.assertEqual(str(package.package), str(package))
        self.assertEqual('Packages', package._meta.verbose_name_plural)

class ScanErrorTestCase(TestCase):
    def test_scan_error_added(self):
        scan_info = ScanInfo.objects.create(scan_type='localscan', is_complete=False)
        code_info = CodeInfo.objects.create(total_code_files=2000, code_size=4096, scan_info=scan_info)
        result = {'scanned_json_result': 'some result',
                  'scanned_html_result': '<h1>HTML result</h1>',
                  'scancode_notice': 'Some dummy notice',
                  'scancode_version': '2.0.0rc3',
                  'files_count': 200,
                  'total_errors': 0,
                  'scan_time': 5000}
        scan_result = ScanResult.objects.create(
            code_info = code_info,
            scanned_json_result = result['scanned_json_result'],
            scanned_html_result = result['scanned_html_result'],
            scancode_notice = result['scancode_notice'],
            scancode_version = result['scancode_version'],
            files_count = result['files_count'],
            total_errors = result['total_errors'],
            scan_time = result['scan_time']
        )
        scan_file_info = ScanFileInfo.objects.create(scan_result=scan_result, file_path='/home/nexb/server/')
        scan_error = ScanError.objects.create(scan_file_info=scan_file_info, scan_error='Integration Issue')
        self.assertEqual('Integration Issue', scan_error.scan_error)
        self.assertEqual(str(scan_error.scan_error), str(scan_error))
        self.assertEqual('Scan Errors', scan_error._meta.verbose_name_plural)
