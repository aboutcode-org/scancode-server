from django.shortcuts import render

# Upload forms from scanapp/forms.py 
from scanapp.forms import URLScanForm
from scanapp.forms import LocalScanForm

# Imports for class based views
from django.views.generic.edit import FormView


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
    success_url = '/thanks/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # files will be uploaded 
            # use following functions to handle
            #handle_uploaded_file(request.FILES['file'])
            pass
