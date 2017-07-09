from django.core.files import File
from django.test import TestCase
from django.test import RequestFactory

from scanapp.views import LocalUploadView
from scanapp.views import URLFormView

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
