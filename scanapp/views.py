# To store the files on the server we use this import
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render

# Upload forms from scanapp/forms.py 
from scanapp.forms import URLScanForm
from scanapp.forms import LocalScanForm

# Imports for class based views
from django.views.generic.edit import FormView

# Import the file that apply scans
from scanapp.tasks import ScanCode

# Only for testing
from django.http import HttpResponse

# Create your views here.
class URLFormView(FormView):
    template_name = 'scanapp/urlscan.html'
    form_class = URLScanForm
    success_url = '/thanks/'
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            # get the code into the file system
            # run the scan
            pass

class LocalUploadView(FormView):
    template_name = 'scanapp/localupload.html'
    form_class = LocalScanForm
    #success_url = '/thanks/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            
            def handle_upload_files(f):

                # store the files on the server
                fs = FileSystemStorage()
                filename = fs.save(f.name, f)
                scan_code = ScanCode()
                json = scan_code.apply_scan('media/'+str(f.name))
                f = '<h1>' + str(json) + '</h1>'
                return f


            # files will be uploaded 
            # use following functions to handle
            return HttpResponse(handle_upload_files(request.FILES['upload_from_local']))

