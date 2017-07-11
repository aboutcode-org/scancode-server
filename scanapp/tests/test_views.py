from django.core.files import File
from django.test import TestCase
from django.test import RequestFactory

from scanapp.views import LocalUploadView
from scanapp.views import URLFormView
from scanapp.views import ScanResults
from scanapp.views import LoginView

from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser

class URLFormViewTestCase(TestCase):
    def test_url_form_view_anonymous_user_get_request(self):
        request = RequestFactory().get('/urlscan/')
        request.user = AnonymousUser()
        response = URLFormView.as_view()(request)
        self.assertEqual(200, response.status_code)
       
    def test_url_form_view_registered_user_get_request(self):
        user = User.objects.create_user(username='username', password='Password')
        request = RequestFactory().get('/urlscan/')
        request.user = user
        response = URLFormView.as_view()(request)
        self.assertEqual(200, response.status_code)

    def test_url_form_view_anonymous_user_post_request_redirects(self):
        request = RequestFactory().post('/urlscan/', {'URL': 'https://github.com'})
        request.user = AnonymousUser()
        response = URLFormView.as_view()(request)
        self.assertEqual(302, response.status_code)

    def test_url_form_view_registered_user_post_request_redirects(self):
        user = User.objects.create_user(username='username', password='Password')
        request = RequestFactory().post('/urlscan/', {'URL': 'https://github.com/'})
        request.user = user
        response = URLFormView.as_view()(request)
        self.assertEqual(302, response.status_code)

    def test_url_form_view_anonymous_user_wrong_post_request(self):
        request = RequestFactory().post('/urlscan/', {'URL': 'https://github'})
        request.user = AnonymousUser()
        response = URLFormView.as_view()(request)
        self.assertIsNone(response)

    def test_url_form_view_anonymous_user_blank_post_request(self):
        request = RequestFactory().post('/urlscan/')
        request.user = AnonymousUser()
        response = URLFormView.as_view()(request)
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

    def test_local_upload_view_anonymous_user_wrong_post_request(self):
        request = RequestFactory().post('/localscan/', {'upload_from_local': File(open('manapy', 'r'))})
        #FIXME gives file doesn't exist error        
        request.user = AnonymousUser()
        response = LocalUploadView.as_view()(request)
        self.assertIsNone(response)

    def test_local_upload_view_anonymous_user_blank_post_request(self):
        request = RequestFactory().post('/localscan/')
        request.user = AnonymousUser()
        response = LocalUploadView.as_view()(request)
        self.assertIsNone(response)

class ScanResultViewTestCase(TestCase):
    def test_scan_result_view_anonymous_user_get_request(self):
        request = RequestFactory().post('/urlscan/', {'URL': 'https://github.com/'})
        request.user = AnonymousUser()
        response = URLFormView.as_view()(request)
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
        request = RequestFactory().post('/urlscan/', {'URL': 'https://github.com/'})
        request.user = AnonymousUser()
        response = URLFormView.as_view()(request)
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
        request = RequestFactory().post('/urlscan/', {'URL': 'https://github.com/'})
        request.user = user
        response = URLFormView.as_view()(request)
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

    def test_login_view_registered_user_get_request(self):
        user = User.objects.create_user(username='Username', password='Password')
        request = RequestFactory().get('/login')
        request.user = user
        response = LoginView.as_view()(request)
        #FIXME login_view must not be accesible to logged in user and it should redirect
        self.assertEqual(302, response.status_code)

    def test_login_view_anonymous_user_post_request(self):
        user = User.objects.create_user(username='username', password='password')
        request = RequestFactory().post('/login', {'username': 'username', 'password': 'password'})
        response = LoginView.as_view()(request)
        self.assertEqual(str(response.context['user']), 'username')
