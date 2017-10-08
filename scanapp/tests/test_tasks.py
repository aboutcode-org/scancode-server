#
# Copyright (c) 2017 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-server/ The
# scancode-server software is licensed under the Apache License version 2.0.
#  Data generated with scancode-server require an acknowledgment.
#
# You may not use this software except in compliance with the License. You
# may obtain a copy of the License at:
# http://apache.org/licenses/LICENSE-2.0 Unless required by applicable law
# or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
#  governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with scancode-server or
# any scancode-server derivative work, you must accompany this data with the
#  following acknowledgment:
#
# Generated with scancode-server and provided on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. No
# content created from scancode-server should be considered or used as legal
#  advice. Consult an Attorney for any legal advice. scancode-server is a
# free software code scanning tool from nexB Inc. and others. Visit
# https://github.com/nexB/scancode-server/ for support and download.

import json

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.utils import timezone

from scanapp.tasks import apply_scan_async
from scanapp.tasks import create_scan_id
from scanapp.tasks import fill_unfilled_scan_model
from scanapp.tasks import save_results_to_db
from scanapp.tasks import scan_code_async

from scanapp.models import Scan
from scanapp.models import ScannedFile
from scanapp.models import License


class CreateScanIdTestCase(TestCase):
    def test_create_scan_id_anonymous_user(self):
        user = None
        url = 'https://github.com'
        scan_directory = 'media/url'
        scan_start_time = timezone.now()
        scan_id = create_scan_id(
            user=user,
            url=url,
            scan_directory=scan_directory,
            scan_start_time=scan_start_time
        )
        self.assertEqual(url, Scan.objects.get(pk=scan_id).url)

    def test_create_scan_id_registered_user(self):
        user = User.objects.create_user(username='username',
                                        password='password')
        url = 'https://github.com'
        scan_directory = 'media/user'
        scan_start_time = timezone.now()
        scan_id = create_scan_id(
            user=user,
            url=url,
            scan_directory=scan_directory,
            scan_start_time=scan_start_time
        )
        self.assertEqual(user.username,
                         Scan.objects.get(pk=scan_id).user.username)
