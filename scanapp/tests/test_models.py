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

import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from scanapp.models import Copyright
from scanapp.models import CopyrightAuthor
from scanapp.models import CopyrightHolder
from scanapp.models import CopyrightStatement
from scanapp.models import License
from scanapp.models import Package
from scanapp.models import Scan
from scanapp.models import ScanError
from scanapp.models import ScannedFile


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
        self.assertEqual('2.0.0rc3', Scan.objects.get(pk=scan.pk).scancode_version)
        self.assertEqual(scan.url, str(Scan.objects.get(pk=scan.pk)))
        self.assertEqual('scans', scan._meta.verbose_name_plural)


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
        scanned_file = ScannedFile.objects.create(
            scan=scan,
            path='/home/nexb/server/',
            type= 'file',
            name= 'celery.py',
            base_name= 'celery',
            extension='.py',
            date=timezone.now(),
            size=1906,
            sha1='2d3c6c804b356a3ef976295fe615e7892dd1e66c',
            md5='1db2f0bc0920084fc0608fab696281ef',
            mime_type='text/x-python',
            file_type='Python script, ASCII text executable',
            programming_language='Python',
            is_binary=False,
            is_text=True,
            is_archive=False,
            is_media=False,
            is_source=True,
            is_script=True
        )

        self.assertEqual('/home/nexb/server/', ScannedFile.objects.get(scan=scan).path)
        self.assertEqual(scanned_file.path, str(ScannedFile.objects.get(scan=scan).path))
        self.assertEqual('scanned files', scanned_file._meta.verbose_name_plural)


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
        scanned_file = ScannedFile.objects.create(
            scan=scan,
            path='/home/nexb/server/',
            type= 'file',
            name= 'celery.py',
            base_name= 'celery',
            extension='.py',
            date=timezone.now(),
            size=1906,
            sha1='2d3c6c804b356a3ef976295fe615e7892dd1e66c',
            md5='1db2f0bc0920084fc0608fab696281ef',
            mime_type='text/x-python',
            file_type='Python script, ASCII text executable',
            programming_language='Python',
            is_binary=False,
            is_text=True,
            is_archive=False,
            is_media=False,
            is_source=True,
            is_script=True
        )
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
        self.assertEqual('mit', License.objects.get(scanned_file=scanned_file).owner)
        self.assertEqual(license.key, str(License.objects.get(scanned_file=scanned_file)))
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
        scanned_file = ScannedFile.objects.create(
            scan=scan,
            path='/home/nexb/server/',
            type= 'file',
            name= 'celery.py',
            base_name= 'celery',
            extension='.py',
            date=timezone.now(),
            size=1906,
            sha1='2d3c6c804b356a3ef976295fe615e7892dd1e66c',
            md5='1db2f0bc0920084fc0608fab696281ef',
            mime_type='text/x-python',
            file_type='Python script, ASCII text executable',
            programming_language='Python',
            is_binary=False,
            is_text=True,
            is_archive=False,
            is_media=False,
            is_source=True,
            is_script=True
        )
        copyright = Copyright.objects.create(
            scanned_file=scanned_file,
            start_line=800,
            end_line=1000
        )
        self.assertEqual(1000, Copyright.objects.get(scanned_file=scanned_file).end_line)
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
        scanned_file = ScannedFile.objects.create(
            scan=scan,
            path='/home/nexb/server/',
            type= 'file',
            name= 'celery.py',
            base_name= 'celery',
            extension='.py',
            date=timezone.now(),
            size=1906,
            sha1='2d3c6c804b356a3ef976295fe615e7892dd1e66c',
            md5='1db2f0bc0920084fc0608fab696281ef',
            mime_type='text/x-python',
            file_type='Python script, ASCII text executable',
            programming_language='Python',
            is_binary=False,
            is_text=True,
            is_archive=False,
            is_media=False,
            is_source=True,
            is_script=True
        )
        copyright = Copyright.objects.create(
            scanned_file=scanned_file,
            start_line=800,
            end_line=1000
        )
        copyright_holder = CopyrightHolder.objects.create(copyright=copyright, holder='mit')

        self.assertEqual('mit', CopyrightHolder.objects.get(copyright=copyright).holder)
        self.assertEqual(copyright_holder.holder, str(CopyrightHolder.objects.get(copyright=copyright).holder))
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
        scanned_file = ScannedFile.objects.create(
            scan=scan,
            path='/home/nexb/server/',
            type= 'file',
            name= 'celery.py',
            base_name= 'celery',
            extension='.py',
            date=timezone.now(),
            size=1906,
            sha1='2d3c6c804b356a3ef976295fe615e7892dd1e66c',
            md5='1db2f0bc0920084fc0608fab696281ef',
            mime_type='text/x-python',
            file_type='Python script, ASCII text executable',
            programming_language='Python',
            is_binary=False,
            is_text=True,
            is_archive=False,
            is_media=False,
            is_source=True,
            is_script=True
        )
        copyright = Copyright.objects.create(
            scanned_file=scanned_file,
            start_line=800,
            end_line=1000
        )
        copyright_statement = CopyrightStatement.objects.create(
            copyright=copyright,
            statement='mit copyright statement'
        )

        self.assertEqual('mit copyright statement', CopyrightStatement.objects.get(copyright=copyright).statement)
        self.assertEqual(copyright_statement.statement, str(CopyrightStatement.objects.get(copyright=copyright)))
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
        scanned_file = ScannedFile.objects.create(
            scan=scan,
            path='/home/nexb/server/',
            type= 'file',
            name= 'celery.py',
            base_name= 'celery',
            extension='.py',
            date=timezone.now(),
            size=1906,
            sha1='2d3c6c804b356a3ef976295fe615e7892dd1e66c',
            md5='1db2f0bc0920084fc0608fab696281ef',
            mime_type='text/x-python',
            file_type='Python script, ASCII text executable',
            programming_language='Python',
            is_binary=False,
            is_text=True,
            is_archive=False,
            is_media=False,
            is_source=True,
            is_script=True
        )
        copyright = Copyright.objects.create(
            scanned_file=scanned_file,
            start_line=800,
            end_line=1000
        )
        copyright_author = CopyrightAuthor.objects.create(
            copyright=copyright,
            author='Ranvir Singh'
        )

        self.assertEqual('Ranvir Singh', CopyrightAuthor.objects.get(copyright=copyright).author)
        self.assertEqual(copyright_author.author, str(CopyrightAuthor.objects.get(copyright=copyright)))
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
        scanned_file = ScannedFile.objects.create(
            scan=scan,
            path='/home/nexb/server/',
            type= 'file',
            name= 'celery.py',
            base_name= 'celery',
            extension='.py',
            date=timezone.now(),
            size=1906,
            sha1='2d3c6c804b356a3ef976295fe615e7892dd1e66c',
            md5='1db2f0bc0920084fc0608fab696281ef',
            mime_type='text/x-python',
            file_type='Python script, ASCII text executable',
            programming_language='Python',
            is_binary=False,
            is_text=True,
            is_archive=False,
            is_media=False,
            is_source=True,
            is_script=True
        )
        package = Package.objects.create(scanned_file=scanned_file, package='bootstrap')

        self.assertEqual('bootstrap', Package.objects.get(scanned_file=scanned_file).package)
        self.assertEqual(package.package, str(Package.objects.get(scanned_file=scanned_file)))
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
        scanned_file = ScannedFile.objects.create(
            scan=scan,
            path='/home/nexb/server/',
            type= 'file',
            name= 'celery.py',
            base_name= 'celery',
            extension='.py',
            date=timezone.now(),
            size=1906,
            sha1='2d3c6c804b356a3ef976295fe615e7892dd1e66c',
            md5='1db2f0bc0920084fc0608fab696281ef',
            mime_type='text/x-python',
            file_type='Python script, ASCII text executable',
            programming_language='Python',
            is_binary=False,
            is_text=True,
            is_archive=False,
            is_media=False,
            is_source=True,
            is_script=True
        )
        scan_error = ScanError.objects.create(
            scanned_file=scanned_file,
            scan_error='Integration Issue'
        )
        self.assertEqual('Integration Issue', ScanError.objects.get(scanned_file=scanned_file).scan_error)
        self.assertEqual(scan_error.scan_error, str(ScanError.objects.get(scanned_file=scanned_file)))
        self.assertEqual('scan errors', scan_error._meta.verbose_name_plural)
