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

# To store the files on the server we use this import
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from scanapp.forms import LocalScanForm
from scanapp.forms import URLScanForm

from scanapp.tasks import scan_code_async
from scanapp.tasks import apply_scan_async

from scanapp.models import CeleryScan

class LocalUploadView(FormView):
    template_name = 'scanapp/localupload.html'
    form_class = LocalScanForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            f = request.FILES['upload_from_local']
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)

            celery_scan = CeleryScan(scan_results='', is_complete=False)
            celery_scan.save()

            scan_id = celery_scan.scan_id

            path = 'media/' + str(filename)
            result = apply_scan_async.delay(path, scan_id)

            # return the response as HttpResponse
            return HttpResponseRedirect('/resultscan/' + str(scan_id))


class URLFormViewCelery(FormView):
    template_name = 'scanapp/urlscan.html'
    form_class = URLScanForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # get the URL from the form
            URL = request.POST['URL']

            celery_scan = CeleryScan(scan_results='', is_complete=False)
            celery_scan.save()

            scan_id = celery_scan.scan_id
            # create the object so scan can be applied
            result = scan_code_async.delay(URL, scan_id)

            # return the response as HttpResponse
            return HttpResponseRedirect('/resultscan/' + str(scan_id))

class ScanResults(TemplateView):
    template_name = 'scanapp/scanresult.html'
    def get(self, request, *args, **kwargs):
        celery_scan = CeleryScan.objects.get(scan_id=kwargs['pk'])
        result = 'Please wait... Your tasks are in the queue.<br/> Reload in 5-10 minutes'
        if celery_scan.is_complete == True:
            result = celery_scan.scan_results

        return render(request, 'scanapp/scanresults.html', context = {'result': result})
