from django.conf.urls import url

from django.views.generic import TemplateView

# import views from scanapp/views.py
from scanapp.views import URLFormView
from scanapp.views import LocalUploadView
from scanapp.views import URLFormViewCelery
from scanapp.views import ScanResults

urlpatterns = [
    url(r'^index/', TemplateView.as_view(template_name="scanapp/index.html")),
    url(r'^urlscan/', URLFormView.as_view(), name='urlformview'),
    url(r'^localscan/', LocalUploadView.as_view(), name='localuploadview'),
    url(r'^urlscannew/', URLFormViewCelery.as_view(), name='urlceleryformview'),
    url(r'^resultscan/(?P<pk>[0-9]+)', ScanResults.as_view(), name='resultview'),
]
