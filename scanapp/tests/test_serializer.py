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
from django.core import serializers
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

from scanapp.serializers import AllModelSerializerHelper
from scanapp.serializers import AllModelSerializer


class AllModelSerializerHelperTestCase(TestCase):
    def test_all_model_serializer_helper(self):
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
        copyright = Copyright.objects.create(
            scanned_file=scanned_file,
            start_line=800,
            end_line=1000
        )
        copyright_holder = CopyrightHolder.objects.create(
            copyright=copyright,
            holder='Ranvir Singh'
        )
        copyright_statement = CopyrightStatement.objects.create(
            copyright=copyright,
            statement='mit copyright statement'
        )
        copyright_author = CopyrightAuthor.objects.create(
            copyright=copyright,
            author='Ranvir Singh'
        )
        package = Package.objects.create(scanned_file=scanned_file, package='bootstrap')
        scan_error = ScanError.objects.create(
            scanned_file=scanned_file,
            scan_error='Integration Issue'
        )

        scan_serializer_helper = AllModelSerializerHelper(scan)
        scan_id = scan.pk
        self.assertEqual(scan_serializer_helper.scan, Scan.objects.get(pk=scan_id))
        self.assertEqual(
            str(scan_serializer_helper.scanned_file),
            str(ScannedFile.objects.filter(scan=Scan.objects.get(pk=scan_id))))
        self.assertEqual(
            str(scan_serializer_helper.license),
            str(
                License.objects.filter(
                    scanned_file=ScannedFile.objects.get(
                        scan=Scan.objects.get(pk=scan_id)
                    )
                )
            )
        )
        self.assertEqual(
            str(scan_serializer_helper.copyright),
            str(
                Copyright.objects.filter(
                    scanned_file=ScannedFile.objects.get(
                        scan=Scan.objects.get(pk=scan_id)
                    )
                )
            )
        )
        self.assertEqual(
            str(scan_serializer_helper.copyright_holder),
            str(
                CopyrightHolder.objects.filter(
                    copyright=Copyright.objects.filter(
                        scanned_file=ScannedFile.objects.get(
                            scan=Scan.objects.get(pk=scan_id)
                        )
                    )
                )
            )
        )
        self.assertEqual(
            str(scan_serializer_helper.copyright_statement),
            str(
                CopyrightStatement.objects.filter(
                    copyright=Copyright.objects.filter(
                        scanned_file=ScannedFile.objects.get(
                            scan=Scan.objects.get(pk=scan_id)
                        )
                    )
                )
            )
        )
        self.assertEqual(
            str(scan_serializer_helper.copyright_author),
            str(
                CopyrightAuthor.objects.filter(
                    copyright=Copyright.objects.filter(
                        scanned_file=ScannedFile.objects.get(
                            scan=Scan.objects.get(pk=scan_id)
                        )
                    )
                )
            )
        )
        self.assertEqual(
            str(scan_serializer_helper.package),
            str(
                Package.objects.filter(
                    scanned_file=ScannedFile.objects.get(
                        scan=Scan.objects.get(pk=scan_id)
                    )
                )
            )
        )
        self.assertEqual(
            str(scan_serializer_helper.scan_error),
            str(
                ScanError.objects.filter(
                    scanned_file=ScannedFile.objects.get(
                        scan=Scan.objects.get(pk=scan_id)
                    )
                )
            )
        )

class AllModelSerializerTestCase(TestCase):
    def test_all_model_serializer(self):
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
        copyright = Copyright.objects.create(
            scanned_file=scanned_file,
            start_line=800,
            end_line=1000
        )
        copyright_holder = CopyrightHolder.objects.create(
            copyright=copyright,
            holder='Ranvir Singh'
        )
        copyright_statement = CopyrightStatement.objects.create(
            copyright=copyright,
            statement='mit copyright statement'
        )
        copyright_author = CopyrightAuthor.objects.create(
            copyright=copyright,
            author='Ranvir Singh'
        )
        package = Package.objects.create(scanned_file=scanned_file, package='bootstrap')
        scan_error = ScanError.objects.create(
            scanned_file=scanned_file,
            scan_error='Integration Issue'
        )

        scan_serializer_helper = AllModelSerializerHelper(scan)
        scan_serializer = AllModelSerializer(scan_serializer_helper)
        scan_serializer_data = """{
            "scan": {
                "id": 13,
                "url": "https;//github.com",
                "scan_directory": "media/username",
                "scancode_notice": "Some dummy notice",
                "scancode_version": "2.0.0rc3",
                "files_count": 200,
                "user": 12
            },
            "scanned_file": [{
                "path": "/home/nexb/server/"
            }],
            "license": [{
                "key": "A",
                "score": 78,
                "short_name": "mit",
                "category": "some category",
                "owner": "mit",
                "homepage_url": "https://github.com/",
                "text_url": "http://github.com/",
                "dejacode_url": "https://github.com",
                "spdx_license_key": "mit",
                "spdx_url": "https://github.com/",
                "start_line": 21, "end_line": 567,
                "matched_rule": {"url": ["https://github.com", "https://google.com"]}
            }],
            "copyright": [{"start_line": 800, "end_line": 1000}],
            "copyright_holder": [{"holder": "Ranvir Singh"}],
            "copyright_statement": [{"statement": "mit copyright statement"}],
            "copyright_author": [{"author": "Ranvir Singh"}],
            "package": [{"package": "bootstrap"}],
            "scan_error": [{"scan_error": "Integration Issue"}]
        }
        """
        self.assertEqual(json.loads(scan_serializer_data)['scanned_file'], scan_serializer.data['scanned_file'])
        self.assertEqual(json.loads(scan_serializer_data)['license'], scan_serializer.data['license'])
        self.assertEqual(json.loads(scan_serializer_data)['copyright'], scan_serializer.data['copyright'])
        self.assertEqual(json.loads(scan_serializer_data)['copyright_holder'], scan_serializer.data['copyright_holder'])
        self.assertEqual(json.loads(scan_serializer_data)['copyright_statement'], scan_serializer.data['copyright_statement'])
        self.assertEqual(json.loads(scan_serializer_data)['copyright_author'], scan_serializer.data['copyright_author'])
        self.assertEqual(json.loads(scan_serializer_data)['package'], scan_serializer.data['package'])
        self.assertEqual(json.loads(scan_serializer_data)['scan_error'], scan_serializer.data['scan_error'])
        key_one = 'scan_start_time'
        key_two = 'scan_end_time'
        del scan_serializer.data['scan'][key_one]
        del scan_serializer.data['scan'][key_two]
        self.assertEqual(json.loads(scan_serializer_data)['scan'], scan_serializer.data['scan'])
