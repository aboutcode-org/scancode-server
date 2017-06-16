from django.conf.urls import url

# upload from scanapp/views 
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^index/', TemplateView.as_view(template_name="scanapp/index.html"))
]
