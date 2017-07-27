# Create your tests here.
import os
import sys

from django.conf import settings
from django.test import TestCase
from django.test.utils import get_runner

from scanapp.forms import URLScanForm

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['your_app'])
    sys.exit(bool(failures))


class URLScanFormTests(TestCase):
    # Valid Form Data
    def test_URLForm_valid(self):
        form_data = {'URL': 'https://github.com/RajuKoushik/Automated-Login.git'}
        form = URLScanForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_URLForm_invalid(self):
        form_data = {'URL': 'randomtestirrelevantdata'}
        form = URLScanForm(data=form_data)
        self.assertFalse(form.is_valid())

    # Valid Response
    def test_add_admin_form_view(self):
        response = self.client.post("/scanurl/",
                                    {'URL': 'https://github.com/RajuKoushik/Automated-Login.git'
                                     })

        self.assertEqual(response.status_code, 302)