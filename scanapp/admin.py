#
# Copyright (c) 2017 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-server/
# The scancode-server software is licensed under the Apache License version 2.0.
# Data generated with scancode-server require an acknowledgment.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with scancode-server or any scancode-server
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with scancode-server and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  scancode-server should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  scancode-server is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-server/ for support and download.

from django.contrib import admin

# Import models from scanapp.models
from .models import UserInfo
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
