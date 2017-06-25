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
