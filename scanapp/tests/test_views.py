from django.test import TestCase

from scanapp.views import LocalUploadView
from scanapp.views import URLFormView

from django.contrib.auth.models import User

class URLFormViewTestCase(TestCase):
    def test_url_form_view_anonymous_user_get_request(self):
        response = self.client.get('/urlscan/')
        self.assertEqual(200, response.status_code)
       
    def test_url_form_view_registered_user_get_request(self):
        user = User.objects.create_user(username='username', password='Password')
        self.client.login(username='username', password='Password')
        response = self.client.get('/urlscan/')
        self.assertEqual('username', str(response.context['user'].username))

    def test_url_form_view_anonymous_user_post_request(self):
        response = self.client.post('/urlscan/', {'URL': 'https://github.com'})
        self.assertEqual(302, response.status_code)

    def test_url_form_view_registered_user_post_request(self):
        user = User.object.create_user(username='username', password='Password')
        self.client.login(username='username', password='Password')
        response = self.client.post('/urlscan/', {'URL': 'https://github.com'})
        self.assertEqual('username', str(response.context['user'].password))
