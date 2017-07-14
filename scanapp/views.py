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
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from scanapp.forms import LocalScanForm
from scanapp.forms import URLScanForm
from scanapp.models import CodeInfo
from scanapp.models import ScanInfo
from scanapp.models import ScanResult
from scanapp.tasks import InsertIntoDB
from scanapp.tasks import apply_scan_async
from scanapp.tasks import scan_code_async

from django.views.decorators.csrf import csrf_exempt
from . import models
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
import json
from django.db import transaction
from django.contrib.auth.models import User
from django.views import View
import subprocess
from tasks import save_results_to_db

from tasks import scan_code_async_special

from os.path import expanduser
import os, shutil

import git


class LocalUploadView(FormView):
    template_name = 'scanapp/localupload.html'
    form_class = LocalScanForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            f = request.FILES['upload_from_local']
            fs = FileSystemStorage('media/AnonymousUser/')
            filename = fs.save(f.name, f)

            scan_type = 'localscan'

            # Create an Instance of InsertIntoDB
            insert_into_db = InsertIntoDB()

            # call the create_scan_id function
            scan_id = insert_into_db.create_scan_id(scan_type)

            # different paths for both anonymous and registered users
            if (str(request.user) == 'AnonymousUser'):
                path = 'media/AnonymousUser/' + str(filename)

            else:
                path = 'media/user/' + str(request.user) + '/' + str(filename)
            folder_name = filename,
            URL = None
            # call the celery function to apply the scan
            apply_scan_async.delay(path, scan_id, scan_type, URL, folder_name)

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

            scan_type = 'URL'

            # Create an Instance of InsertIntoDB
            insert_into_db = InsertIntoDB()

            # call the create_scan_id function
            scan_id = insert_into_db.create_scan_id(scan_type)

            # different paths for both anonymous and registered users
            if (str(request.user) == 'AnonymousUser'):
                path = 'media/AnonymousUser/URL/'

            else:
                path = 'media/user/' + str(request.user) + '/URL/'

            scan_code_async.delay(URL, scan_id, path)
            # return the response as HttpResponse
            return HttpResponseRedirect('/resultscan/' + str(scan_id))


class ScanResults(TemplateView):
    template_name = 'scanapp/scanresult.html'

    def get(self, request, *args, **kwargs):
        # celery_scan = CeleryScan.objects.get(scan_id=kwargs['pk'])
        scan_info = ScanInfo.objects.get(pk=kwargs['pk'])
        result = 'Please wait... Your tasks are in the queue.\n Reload in 5-10 minutes'
        if scan_info.is_complete == True:
            code_info = CodeInfo.objects.get(scan_info=scan_info)
            scan_result = ScanResult.objects.get(code_info=code_info)
            result = scan_result.scanned_json_result

        return render(request, 'scanapp/scanresults.html', context={'result': result})


class LoginView(TemplateView):
    template_name = "scanapp/login.html"


class RegisterView(View):
    def post(self, request):
        if request.POST.get('password') != request.POST.get('confirm-password'):
            return HttpResponse("Unauthorized- Password doesn't match", status=401)

        with transaction.atomic():
            user = User.objects.create_user(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                email=request.POST.get('email')
            )

            user.save()

        return HttpResponse(
            json.dumps(
                {
                    'token': Token.objects.get(user=user).key
                }
            )
        )


class UrlScanSpecialView(FormView):
    template_name = 'scanapp/urlspecialscan.html'
    form_class = URLScanForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # get the URL from the form
            URL = request.POST['URL']

            scan_type = 'SpecialURL'

            dir_name = 'temp'

            home_path = expanduser("~")

            os.chdir(home_path)

            if os.path.isdir(dir_name):
                shutil.rmtree(dir_name)

            os.mkdir(dir_name)

            repo = git.Repo.init(dir_name)
            origin = repo.create_remote('origin', URL)
            origin.fetch()
            origin.pull(origin.refs[0].remote_head)

            print "Done ! Remote repository cloned."

            # Create an Instance of InsertIntoDB
            insert_into_db = InsertIntoDB()

            # call the create_scan_id function
            scan_id = insert_into_db.create_scan_id(scan_type)

            filename = home_path + '/temp/'

            # print filename

            path = filename

            folder_name = filename,
            URL = None

            scan_result = subprocess.check_output(['scancode', filename])
            json_data = json.loads(scan_result)
            return HttpResponse(
                json.dumps(
                    {
                        'json': json_data
                    }
                )
            )
