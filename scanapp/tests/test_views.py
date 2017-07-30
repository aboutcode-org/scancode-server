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

from django.core.files import File
from django.test import TestCase
from django.test import RequestFactory

from scanapp.views import LocalUploadView
from scanapp.views import UrlScanView
from scanapp.views import ScanResults
from scanapp.views import LoginView

from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser


class UrlScanViewTestCase(TestCase):
    def test_url_scan_view_anonymous_user_get_request(self):
        request = RequestFactory().get('/urlscan/')
        request.user = AnonymousUser()
        response = UrlScanView.as_view()(request)
        self.assertEqual(200, response.status_code)
       
    def test_url_scan_view_registered_user_get_request(self):
        user = User.objects.create_user(username='username', password='Password')
        request = RequestFactory().get('/urlscan/')
        request.user = user
        response = UrlScanView.as_view()(request)
        self.assertEqual(200, response.status_code)

    def test_url_scan_view_anonymous_user_post_request_redirects(self):
        request = RequestFactory().post('/urlscan/', {'url': 'https://github.com'})
        request.user = AnonymousUser()
        response = UrlScanView.as_view()(request)
        self.assertEqual(302, response.status_code)

    def test_url_scan_view_registered_user_post_request_redirects(self):
        user = User.objects.create_user(username='username', password='Password')
        request = RequestFactory().post('/urlscan/', {'url': 'https://github.com/'})
        request.user = user
        response = UrlScanView.as_view()(request)
        self.assertEqual(302, response.status_code)

    def test_url_scan_view_anonymous_user_wrong_post_request(self):
        request = RequestFactory().post('/urlscan/', {'url': 'https://github'})
        request.user = AnonymousUser()
        response = UrlScanView.as_view()(request)
        self.assertIsNone(response)

    def test_url_scan_view_anonymous_user_blank_post_request(self):
        request = RequestFactory().post('/urlscan/')
        request.user = AnonymousUser()
        response = UrlScanView.as_view()(request)
        self.assertIsNone(response)


class LocalUploadViewTestCase(TestCase):
    def test_local_form_view_anonymous_user_get_request(self):
        request = RequestFactory().get('/localscan/')
        request.user = AnonymousUser()
        response = LocalUploadView.as_view()(request)
        self.assertEqual(200, response.status_code)

    def test_local_upload_view_registered_user_get_request(self):
        user = User.objects.create_user(username='username', password='Password')
        request = RequestFactory().get('/localscan/')
        request.user = user
        response = LocalUploadView.as_view()(request)
        self.assertEqual(200, response.status_code)

    def test_local_upload_view_anonymous_user_post_request_redirects(self):
        request = RequestFactory().post('/localscan/', {'upload_from_local': File(open('manage.py', 'r'))})
        request.user = AnonymousUser()
        response = LocalUploadView.as_view()(request)
        self.assertEqual(302, response.status_code)

    def test_local_upload_view_registered_user_post_request_redirects(self):
        user = User.objects.create_user(username='username', password='Password')
        request = RequestFactory().post('/localscan/', {'upload_from_local': File(open('manage.py', 'r'))})
        request.user = user
        response = LocalUploadView.as_view()(request)
        self.assertEqual(302, response.status_code)

#    def test_local_upload_view_anonymous_user_wrong_post_request(self):
#        request = RequestFactory().post('/localscan/', {'upload_from_local': File(open('manapy', 'r'))})
#        #FIXME gives file doesn't exist error
#        request.user = AnonymousUser()
#        response = LocalUploadView.as_view()(request)
#        self.assertIsNone(response)

    def test_local_upload_view_anonymous_user_blank_post_request(self):
        request = RequestFactory().post('/localscan/')
        request.user = AnonymousUser()
        response = LocalUploadView.as_view()(request)
        self.assertIsNone(response)


class ScanResultViewTestCase(TestCase):
    def test_scan_result_view_anonymous_user_get_request(self):
        request = RequestFactory().post('/urlscan/', {'url': 'https://github.com/'})
        request.user = AnonymousUser()
        response = UrlScanView.as_view()(request)
        url = response.url
        digits_in_url = url[12:]
        scan_id = ''
        for character in digits_in_url:
            try:
                scan_id = scan_id + str(int(character))
            except:
                pass
        scan_id = int(scan_id)
        request = RequestFactory().get('/scanresult/')
        response = ScanResults.as_view()(request, pk=scan_id)
        self.assertEqual('<h3>Please wait... Your tasks are in the queue.\n Reload in 5-10 minutes</h3>\n', response.content)

    def test_scan_result_view_anonymous_user_post_request(self):
        request = RequestFactory().post('/urlscan/', {'url': 'https://github.com/'})
        request.user = AnonymousUser()
        response = UrlScanView.as_view()(request)
        url = response.url
        digits_in_url = url[12:]
        scan_id = ''
        for character in digits_in_url:
            try:
                scan_id = scan_id + str(int(character))
            except:
                pass
        scan_id = int(scan_id)
        request = RequestFactory().post('/scanresult/', {'post_apple': 'Apple'})
        response = ScanResults.as_view()(request, pk=scan_id)
        self.assertEqual(405, response.status_code)

    def test_scan_result_view_registered_user_get_request(self):
        user = User.objects.create_user(username='Username', password='Password')
        request = RequestFactory().post('/urlscan/', {'url': 'https://github.com/'})
        request.user = user
        response = UrlScanView.as_view()(request)
        url = response.url
        digits_in_url = url[12:]
        scan_id = ''
        for character in digits_in_url:
            try:
                scan_id = scan_id + str(int(character))
            except:
                pass
        scan_id = int(scan_id)
        request = RequestFactory().get('/scanresult/')
        response = ScanResults.as_view()(request, pk=scan_id)
        self.assertEqual('<h3>Please wait... Your tasks are in the queue.\n Reload in 5-10 minutes</h3>\n', response.content)


class LoginViewTestCase(TestCase):
    def test_login_view_anonymous_user_get_request(self):
        request = RequestFactory().get('/login')
        request.user = AnonymousUser()
        response = LoginView.as_view()(request)
        self.assertEqual(200, response.status_code)

#    def test_login_view_registered_user_get_request(self):
#        user = User.objects.create_user(username='Username', password='Password')
#        request = RequestFactory().get('/login')
#        request.user = user
#        response = LoginView.as_view()(request)
#        #FIXME login_view must not be accesible to logged in user and it should redirect
#        self.assertEqual(302, response.status_code)
#
#    def test_login_view_anonymous_user_post_request(self):
#        user = User.objects.create_user(username='username', password='password')
#        request = RequestFactory().post('/login', {'username': 'username', 'password': 'password'})
#        response = LoginView.as_view()(request)
#        self.assertEqual(str(response.context['user']), 'username')
