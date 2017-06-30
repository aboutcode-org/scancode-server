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

from django.conf.urls import url

from django.views.generic import TemplateView

# import views from scanapp/views.py
from scanapp.views import LocalUploadView
from scanapp.views import URLFormViewCelery
from scanapp.views import ScanResults

urlpatterns = [
    url(r'^index/', TemplateView.as_view(template_name="scanapp/index.html")),
    url(r'^localscan/', LocalUploadView.as_view(), name='localuploadview'),
    url(r'^urlscan/', URLFormViewCelery.as_view(), name='urlceleryformview'),
    url(r'^resultscan/(?P<pk>[0-9]+)', ScanResults.as_view(), name='resultview'),
]
