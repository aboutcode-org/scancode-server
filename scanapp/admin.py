from django.contrib import admin

from .models import user_info, AnonymousUser, code_info, scanned_results, copyright, license, package

# Register your models here.
admin.site.register(user_info)
admin.site.register(AnonymousUser)
admin.site.register(code_info)
admin.site.register(scanned_results)
admin.site.register(copyright)
admin.site.register(license)
admin.site.register(package)
