from django.contrib import admin

# Import models from scanapp.models
from .models import UserInfo
from .models import AnonymousUser
from .models import CodeInfo
from .models import ScanError
from .models import Copyright
from .models import License
from .models import Package
from .models import ScanInfo
from .models import URLScanInfo
from .models import LocalScanInfo
from .models import ScanResult
from .models import ScanFileInfo

# Register models from scancode.models
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
