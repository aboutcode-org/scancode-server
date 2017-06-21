# To store the files on the server we use this import
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.views.generic.edit import FormView

from scanapp.forms import LocalScanForm
from scanapp.forms import URLScanForm
from scanapp.tasks import ScanCode


# Create your views here.
class URLFormView(FormView):
    template_name = 'scanapp/urlscan.html'
    form_class = URLScanForm

    # success_url = '/thanks/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # get the URL from the form
            URL = request.POST['URL']

            # create the object so scan can be applied
            scan_code = ScanCode()
            result = scan_code.get_content(URL)

            # return the response as HttpResponse
            return HttpResponse(result)


class LocalUploadView(FormView):
    template_name = 'scanapp/localupload.html'
    form_class = LocalScanForm

    # success_url = '/thanks/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            def handle_upload_files(f):
                # store the files on the server
                fs = FileSystemStorage()
                filename = fs.save(f.name, f)

                # call the scan function to scan the file recieved
                scan_code = ScanCode()
                result = scan_code.apply_scan('media/' + str(f.name))

                # Handle the data received
                return result

            handle_data = handle_upload_files(request.FILES['upload_from_local'])
            # files will be uploaded 
            # use following functions to handle
            return HttpResponse(handle_data)


class URLFormViewCelery(FormView):
    template_name = 'scanapp/urlscan.html'
    form_class = URLScanForm

    # success_url = '/thanks/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # get the URL from the form
            URL = request.POST['URL']

            # create the object so scan can be applied
            scan_code = ScanCode()
            result = scan_code.get_content(URL)

            # return the response as HttpResponse
            return HttpResponse(result)
