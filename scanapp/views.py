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
import logging
import os
import subprocess

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from giturl import GitURL
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from scanapp.forms import LocalScanForm
from scanapp.forms import UrlScanForm
from scanapp.models import Scan
from scanapp.serializers import AllModelSerializer
from scanapp.serializers import AllModelSerializerHelper
from scanapp.tasks import apply_scan_async
from scanapp.tasks import create_scan_id
from scanapp.tasks import handle_special_urls
from scanapp.tasks import scan_code_async


class LocalUploadView(FormView):
    """
    Handles everything for applyig scan by uploading files from local
    like saving files at right place, Updating database and showing
    file upload forms
    """
    template_name = 'scanapp/localupload.html'
    form_class = LocalScanForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            if (str(request.user) == 'AnonymousUser'):
                path = 'media/AnonymousUser/'
                user = None

            else:
                path = 'media/user/' + str(request.user) + '/'
                user = request.user

            subprocess.call(['mkdir', '-p', path])
            f = request.FILES['upload_from_local']
            fs = FileSystemStorage(path)
            filename = fs.save(f.name, f)

            path = path + str(filename)
            scan_directory = filename
            url = fs.url(filename)
            scan_start_time = timezone.now()
            scan_id = create_scan_id(user, url, scan_directory, scan_start_time)
            apply_scan_async.delay(path, scan_id)

            return HttpResponseRedirect('/resultscan/' + str(scan_id))


class ScanResults(TemplateView):
    template_name = 'scanapp/scanresult.html'

    def get(self, request, *args, **kwargs):
        scan_id = kwargs['pk']
        scan = Scan.objects.get(pk=scan_id)
        result = 'Please wait... Your tasks are in the queue.\n Reload in 5-10 minutes'
        if scan.scan_end_time is not None:
            result = scan

        return render(request, 'scanapp/scanresults.html', context={
            'result': result,
            'scan_id': scan_id,
        })


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


class UrlScanView(FormView):
    template_name = 'scanapp/urlscan.html'
    form_class = UrlScanForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            url = request.POST['url']
            logger = logging.getLogger(__name__)

            if request.user.is_authenticated():
                path = '/'.join(['media', 'user', str(request.user), 'url'])
                user = request.user
            else:
                path = '/'.join(['media', 'AnonymousUser', 'url'])
                user = None

            scan_start_time = timezone.now()
            git_url_parser = GitURL(url)

            if git_url_parser.host == 'github.com':
                file_name = git_url_parser.repo
                scan_directory = file_name
                scan_id = create_scan_id(user, url, scan_directory, scan_start_time)
                current_scan = Scan.objects.get(pk=scan_id)
                path = '/'.join([path, '{}'.format(current_scan.pk), file_name])

                os.makedirs(path)

                handle_special_urls.delay(url, scan_id, path, git_url_parser.host)
                logger.info('git repo detected')
            else:
                scan_directory = None
                scan_id = create_scan_id(user, url, scan_directory, scan_start_time)
                current_scan = Scan.objects.get(pk=scan_id)
                path = '/'.join([path, '{}'.format(current_scan.pk)])

                os.makedirs(path)

                file_name = '{}'.format(current_scan.pk)
                scan_code_async.delay(url, scan_id, path, file_name)

            return HttpResponseRedirect('/resultscan/' + '{}'.format(current_scan.pk))


# API views
class ScanApiView(APIView):
    def get(self, request, format=None, **kwargs):
        scan_id = kwargs['pk']
        scan = Scan.objects.get(pk=scan_id)
        scan_serializer = AllModelSerializerHelper(scan)
        scan_serializer = AllModelSerializer(scan_serializer)
        return Response(scan_serializer.data)
