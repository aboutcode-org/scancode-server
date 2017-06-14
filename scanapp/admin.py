from django.contrib import admin

from .models import UserInfo, AnonymousUser, CodeInfo, ScanError, Copyright, License, Package, ScanInfo, URLScanInfo, \
    LocalScanInfo, ScanResult, ScanFileInfo

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(AnonymousUser)
admin.site.register(CodeInfo)
admin.site.register(ScanError)
admin.site.register(Copyright)
admin.site.register(License)
admin.site.register(Package)
admin.site.register(ScanInfo)
admin.site.register(URLScanInfo)
admin.site.register(LocalScanInfo)
admin.site.register(ScanFileInfo)
admin.site.register(ScanResult)
