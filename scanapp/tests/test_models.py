import json
from django.utils import timezone

from django.test import TestCase

from django.contrib.auth.models import User
from scanapp.models import Scan
from scanapp.models import ScannedFile
from scanapp.models import License
from scanapp.models import Copyright
from scanapp.models import CopyrightHolder
from scanapp.models import CopyrightStatement
from scanapp.models import CopyrightAuthor
from scanapp.models import Package
from scanapp.models import ScanError


class ScanTestCase(TestCase):
    def test_scan_added(self):
        user = User.objects.create_user(username='username', password='password')
        scan = Scan.objects.create(
            user=user,
            url='https;//github.com',
            scan_directory='media/username',
            scancode_notice='Some dummy notice',
            scancode_version='2.0.0rc3',
            files_count=200,
            scan_start_time=timezone.now(),
            scan_end_time=timezone.now()
        )
        
        self.assertEqual('2.0.0rc3', scan.scancode_version)
        self.assertEqual(str(scan.url), str(scan))
        self.assertEqual('scans', str(scan._meta.verbose_name_plural))


class ScannedFileTestCase(TestCase):
    def test_scanned_file_added(self):
        user = User.objects.create_user(username='username', password='password')
        scan = Scan.objects.create(
            user=user,
            url='https;//github.com',
            scan_directory='media/username',
            scancode_notice='Some dummy notice',
            scancode_version='2.0.0rc3',
            files_count=200,
            scan_start_time=timezone.now(),
            scan_end_time=timezone.now()
        )
        scanned_file = ScannedFile.objects.create(scan=scan, path='/home/nexb/server/')

        self.assertEqual('/home/nexb/server/', scanned_file.path)
        self.assertEqual(scanned_file.path, str(scanned_file))
        self.assertEqual('scanned files', str(scanned_file._meta.verbose_name_plural))


class LicenseTestCase(TestCase):
    def test_license_added(self):
        user = User.objects.create_user(username='username', password='password')
        scan = Scan.objects.create(
            user=user,
            url='https;//github.com',
            scan_directory='media/username',
            scancode_notice='Some dummy notice',
            scancode_version='2.0.0rc3',
            files_count=200,
            scan_start_time=timezone.now(),
            scan_end_time=timezone.now()
        )
        scanned_file = ScannedFile.objects.create(scan=scan, path='/home/nexb/server/')
        license = License.objects.create(
            scanned_file=scanned_file, 
            key='A',
            score=78,
            short_name='mit',
            category='some category',
            owner='mit',
            homepage_url='https://github.com/',
            text_url='http://github.com/',
            dejacode_url='https://github.com',
            spdx_license_key='mit', 
            spdx_url='https://github.com/',
            start_line=21,
            end_line=567,
            matched_rule=json.loads('{"url": ["https://github.com", "https://google.com"]}')
        )
        self.assertEqual('mit', license.owner)
        self.assertEqual(license.key, str(license))
        self.assertEqual('licenses', license._meta.verbose_name_plural)


class CopyrightTestCase(TestCase):
    def test_copyright_added(self):
        user = User.objects.create_user(username='username', password='password')
        scan = Scan.objects.create(
            user=user,
            url='https;//github.com',
            scan_directory='media/username',
            scancode_notice='Some dummy notice',
            scancode_version='2.0.0rc3',
            files_count=200,
            scan_start_time=timezone.now(),
            scan_end_time=timezone.now()
        )
        scanned_file = ScannedFile.objects.create(scan=scan, path='/home/nexb/server/')
        copyright = Copyright.objects.create(
            scanned_file=scanned_file,
            start_line=800,
            end_line=1000
        )
        self.assertEqual(1000, copyright.end_line)
        self.assertEqual(str(copyright.start_line), str(copyright))
        self.assertEqual('copyrights', copyright._meta.verbose_name_plural)


class CopyrightHolderTestCase(TestCase):
    def test_copyright_holder_added(self):
        user = User.objects.create_user(username='username', password='password')
        scan = Scan.objects.create(
            user=user,
            url='https;//github.com',
            scan_directory='media/username',
            scancode_notice='Some dummy notice',
            scancode_version='2.0.0rc3',
            files_count=200,
            scan_start_time=timezone.now(),
            scan_end_time=timezone.now()
        )
        scanned_file = ScannedFile.objects.create(scan=scan, path='/home/nexb/server/')
        copyright = Copyright.objects.create(
            scanned_file=scanned_file,
            start_line=800,
            end_line=1000
        )
        copyright_holder = CopyrightHolder.objects.create(copyright=copyright, holder='mit')
        self.assertEqual('mit', copyright_holder.holder)
        self.assertEqual(str(copyright_holder.holder), str(copyright_holder))
        self.assertEqual('copyright holders', copyright_holder._meta.verbose_name_plural)


class CopyrightStatementTestCase(TestCase):
    def test_copyright_statement_added(self):
        user = User.objects.create_user(username='username', password='password')
        scan = Scan.objects.create(
            user=user,
            url='https;//github.com',
            scan_directory='media/username',
            scancode_notice='Some dummy notice',
            scancode_version='2.0.0rc3',
            files_count=200,
            scan_start_time=timezone.now(),
            scan_end_time=timezone.now()
        )
        scanned_file = ScannedFile.objects.create(scan=scan, path='/home/nexb/server/')
        copyright = Copyright.objects.create(
            scanned_file=scanned_file,
            start_line=800,
            end_line=1000
        )
        copyright_statement = CopyrightStatement.objects.create(
            copyright=copyright,
            statement='mit copyright statement'
        )
        self.assertEqual('mit copyright statement', copyright_statement.statement)
        self.assertEqual(str(copyright_statement.statement), str(copyright_statement))
        self.assertEqual('copyright statements', copyright_statement._meta.verbose_name_plural)


class CopyrightAuthorTestCase(TestCase):
    def test_copyright_author_added(self):
        user = User.objects.create_user(username='username', password='password')
        scan = Scan.objects.create(
            user=user,
            url='https;//github.com',
            scan_directory='media/username',
            scancode_notice='Some dummy notice',
            scancode_version='2.0.0rc3',
            files_count=200,
            scan_start_time=timezone.now(),
            scan_end_time=timezone.now()
        )
        scanned_file = ScannedFile.objects.create(scan=scan, path='/home/nexb/server/')
        copyright = Copyright.objects.create(
            scanned_file=scanned_file,
            start_line=800,
            end_line=1000
        )
        copyright_author = CopyrightAuthor.objects.create(
            copyright=copyright,
            author='Ranvir Singh'
        )
        self.assertEqual('Ranvir Singh', copyright_author.author)
        self.assertEqual(str(copyright_author.author), str(copyright_author))
        self.assertEqual('copyright authors', copyright_author._meta.verbose_name_plural)


class PackageTestCase(TestCase):
    def test_package_added(self):
        user = User.objects.create_user(username='username', password='password')
        scan = Scan.objects.create(
            user=user,
            url='https;//github.com',
            scan_directory='media/username',
            scancode_notice='Some dummy notice',
            scancode_version='2.0.0rc3',
            files_count=200,
            scan_start_time=timezone.now(),
            scan_end_time=timezone.now()
        )
        scanned_file = ScannedFile.objects.create(scan=scan, path='/home/nexb/server/')
        package = Package.objects.create(scanned_file=scanned_file, package='bootstrap')
        self.assertEqual('bootstrap', package.package)
        self.assertEqual(str(package.package), str(package))
        self.assertEqual('packages', package._meta.verbose_name_plural)


class ScanErrorTestCase(TestCase):
    def test_scan_error_added(self):
        user = User.objects.create_user(username='username', password='password')
        scan = Scan.objects.create(
            user=user,
            url='https;//github.com',
            scan_directory='media/username',
            scancode_notice='Some dummy notice',
            scancode_version='2.0.0rc3',
            files_count=200,
            scan_start_time=timezone.now(),
            scan_end_time=timezone.now()
        )
        scanned_file = ScannedFile.objects.create(scan=scan, path='/home/nexb/server/')
        scan_error = ScanError.objects.create(
            scanned_file=scanned_file,
            scan_error='Integration Issue'
        )
        self.assertEqual('Integration Issue', scan_error.scan_error)
        self.assertEqual(str(scan_error.scan_error), str(scan_error))
        self.assertEqual('scan errors', scan_error._meta.verbose_name_plural)
