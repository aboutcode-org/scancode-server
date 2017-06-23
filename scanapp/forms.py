from django import forms


class URLScanForm(forms.Form):
    URL = forms.URLField(label='URL', max_length=2000)


class LocalScanForm(forms.Form):
    upload_from_local = forms.FileField(label='Upload from Local')
