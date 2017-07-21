from rest_framework import serializers

from django.contrib.auth.models import User

from scanapp.models import ScanInfo
from scanapp.models import UserInfo
from scanapp.models import URLScanInfo
from scanapp.models import LocalScanInfo
from scanapp.models import CodeInfo
from scanapp.models import ScanResult
from scanapp.models import ScanFileInfo
from scanapp.models import License
from scanapp.models import MatchedRule
from scanapp.models import MatchedRuleLicenses
from scanapp.models import Copyright
from scanapp.models import CopyrightHolders
from scanapp.models import CopyrightStatements
from scanapp.models import CopyrightAuthor
from scanapp.models import Package
from scanapp.models import ScanError


class ScanInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `ScanInfo` model with all fields
    """
    class Meta:
        model = ScanInfo
        exclude = ('id',)


class UserSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `User` model
    """
    class Meta:
        model = User
        exclude = ('id',)


class UserInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `UserInfo` model with all field
    """
    user = UserSerializer()
    class Meta:
        model = UserInfo
        exclude = ('id',)


class UrlScanInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `URLScanInfo` with all fields
    """
    class Meta:
        model = URLScanInfo
        exclude = ('id',)


class LocalScanInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `LocalScanInfo` with all fields
    """
    class Meta:
        model = LocalScanInfo
        exclude = ('id',)

class CodeInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CodeInfo` with all fields
    """
    class Meta:
        model = CodeInfo
        exclude = ('id',)

class ScanResultSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `ScanResult` with all fields
    """
    class Meta:
        model = ScanResult
        exclude = ('id',)

class ScanFileInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `ScanFileInfo` with all fields
    """
    class Meta:
        model = ScanFileInfo
        exclude = ('id',)

class LicenseSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `License` with all fields
    """
    class Meta:
        model = License
        exclude = ('id',)

class MatchedRuleSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `MatchedRule` with all fields
    """
    class Meta:
        model = MatchedRule
        exclude = ('id',)

class MatchedRuleLicenseSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `MatchedRuleLicense` with all fields
    """
    class Meta:
        model = MatchedRuleLicenses
        exclude = ('id',)

class CopyrightSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Copyright` with all fields
    """
    class Meta:
        model = Copyright
        exclude = ('id',)

class CopyrightHolderSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CopyrightHolders` with all fields
    """
    class Meta:
        model = CopyrightHolders
        exclude = ('id',)

class CopyrightStatementSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CopyrightHolders` with all fields
    """
    class Meta:
        model = CopyrightStatements
        exclude = ('id',)

class CopyrightAuthorSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CopyrightAuthor` with all fields
    """
    class Meta:
        model = CopyrightAuthor
        exclude = ('id',)

class PackageSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Package` with all fields
    """
    class Meta:
        model = Package
        exclude = ('id',)

class ScanErrorSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Package` with all fields
    """
    class Meta:
        model = ScanError
        exclude = ('id',)


# writing good code after so much strugle
class GodSerializer(serializers.Serializer):
    """
    Another good serializer to handle all the serialization activities
    """
    code_info = CodeInfoSerializer()
    url_scan = UrlScanInfoSerializer()
    local_scan = LocalScanInfoSerializer()
    scan_result = ScanResultSerializer()
    scan_file_info = ScanFileInfoSerializer(many=True)
    license = LicenseSerializer(many=True)
    matched_rule = MatchedRuleSerializer(many=True)
    matched_rule_license = MatchedRuleLicenseSerializer(many=True)
    copyright = CopyrightSerializer(many=True)
    copyright_holder = CopyrightHolderSerializer(many=True)
    copyright_statement = CopyrightStatementSerializer(many=True)
    copyright_author = CopyrightAuthorSerializer(many=True)
    package = PackageSerializer(many=True)
    scan_error = ScanErrorSerializer(many=True)


class GodSerializerHelper(object):
    def __init__(self, scan_info):
        self.scan_info = scan_info
        self.code_info = CodeInfo.objects.get(scan_info=scan_info)
        self.url_scan = URLScanInfo.objects.get(scan_info=scan_info)
        self.local_scan = None
        self.scan_result = ScanResult.objects.get(code_info=self.code_info)
        self.scan_file_info = ScanFileInfo.objects.filter(scan_result=self.scan_result)
        self.license = License.objects.filter(scan_file_info__in=(self.scan_file_info))
        self.matched_rule = MatchedRule.objects.filter(license__in=(self.license))
        self.matched_rule_license = MatchedRuleLicenses.objects.filter(matched_rule__in=(self.matched_rule))
        self.copyright = Copyright.objects.filter(scan_file_info__in=(self.scan_file_info))
        self.copyright_holder = CopyrightHolders.objects.filter(copyright__in=(self.copyright))
        self.copyright_statement = CopyrightStatements.objects.filter(copyright__in=(self.copyright))
        self.copyright_author = CopyrightAuthor.objects.filter(copyright__in=(self.copyright))
        self.package = Package.objects.filter(scan_file_info__in=(self.scan_file_info))
        self.scan_error = ScanError.objects.filter(scan_file_info__in=(self.scan_file_info))

s = GodSerializerHelper(ScanInfo.objects.get(pk=51))
s = GodSerializer(s)
s.data

### Awesome code ####
from scanapp.models import ScanInfo
from scanapp.models import URLScanInfo
from scanapp.models import LocalScanInfo
from scanapp.models import CodeInfo
from rest_framework import serializers
class CodeScan(object):
    def __init__(self, code_scan_obj):
        self.total_code_files = code_scan_obj.total_code_files
        self.code_size = code_scan_obj.code_size

class LocalScan(object):
    def __init__(self, local_object, scan_info, code_info):
        self.scan_info = scan_info
        self.code_info = code_info
        self.folder_name = local_object.folder_name

class URLScan(object):
    def __init__(self, url_object, scan_info, code_info):
        self.scan_info = scan_info
        self.code_info = code_info
        self.url = url_object.URL

class Scan(object):
    def __init__(self, scan_object):
        self.scan_type = scan_object.scan_type
        self.is_complete = scan_object.is_complete

class ScanSerializer(serializers.Serializer):
    scan_type = serializers.CharField()
    is_complete = serializers.BooleanField()

class CodeScanSerializer(serializers.Serializer):
    total_code_files = serializers.IntegerField()
    code_size = serializers.IntegerField()

class UrlScanSerializer(serializers.Serializer):
    url = serializers.URLField()

class LocalScanSerializer(serializers.Serializer):
    folder_name = serializers.CharField()

#a_scan = Scan(ScanInfo.objects.get(pk=36))
scan_info = ScanInfo.objects.all()
chromo = list()
for a_scan in scan_info:
    b_scan = Scan(a_scan)
    if(a_scan.scan_type == 'URL'):
        try:
            code_info = CodeInfo.objects.get(scan_info=a_scan)
            url_scan_info = URLScan(URLScanInfo.objects.get(scan_info=a_scan), b_scan, code_info)
            serializer = UrlScanSerializer(url_scan_info)
            chromo.append(serializer.data)
        except:
            print("Go on don't worry")
    else:
        try:
            code_info = CodeInfo.objects.get(scan_info=a_scan)
            local_scan_info = LocalScan(LocalScanInfo.objects.get(scan_info=a_scan), a_scan, code_info)
            serializer = LocalScanSerializer(local_scan_info)
            chromo.append(serializer.data)
        except:
            print("Don't worry")

print(chromo)


##### Brilliant code ######
from scanapp.models import ScanInfo
from scanapp.models import URLScanInfo
from scanapp.models import LocalScanInfo
from scanapp.models import CodeInfo
from scanapp.models import ScanResult
from rest_framework import serializers


class CodeScan(object):
    def __init__(self, code_scan_obj):
        self.total_code_files = code_scan_obj.total_code_files
        self.code_size = code_scan_obj.code_size


class Scan(object):
    def __init__(self, scan_object, code_info=None, url_scan=None, local_scan=None, scan_result=None):
        self.scan_type = scan_object.scan_type
        self.is_complete = scan_object.is_complete
        self.code_info = code_info
        self.url_scan = url_scan
        self.local_scan = local_scan
        self.scan_result = scan_result


#TODO check that after removing these things work or not.
class URLScan(object):
    def __init__(self, url_object):
        self.url = url_object.URL


class LocalScan(object):
    def __init__(self, local_object):
        self.folder_name = local_object.folder_name


class UrlScanSerializer(serializers.Serializer):
    url = serializers.URLField()


class LocalScanSerializer(serializers.Serializer):
    folder_name = serializers.CharField()


class ScanResultSerializer(serializers.Serializer):
    scanned_json_result = serializers.JSONField()
    scanned_html_result = serializers.CharField()
    scancode_notice = serializers.CharField()
    scancode_version = serializers.CharField()
    files_count = serializers.IntegerField()
    total_errors = serializers.IntegerField()
    scan_time = serializers.IntegerField()


class ScanSerializer(serializers.Serializer):
    scan_type = serializers.CharField()
    is_complete = serializers.BooleanField()
    code_info = CodeScanSerializer()
    url_scan = UrlScanSerializer()
    local_scan = LocalScanSerializer()
    scan_result = ScanResultSerializer()


scan_info = ScanInfo.objects.all()
chromo = list()
for a_scan in scan_info:
    if(a_scan.scan_type == 'URL'):
        try:
            try:
                code_info = CodeInfo.objects.get(scan_info=a_scan)
                scan_result = ScanResult.objects.get(code_info=code_info)
            except:
                code_info = None
                scan_result = None
            url_scan = URLScan(URLScanInfo.objects.get(scan_info=a_scan)) or None
            local_scan = None
            scan = Scan(a_scan, code_info, url_scan, local_scan, scan_result)
            serializer = ScanSerializer(scan)
            chromo.append(serializer.data)
        except:
            pass
    else:
        try:
            try:
                code_info = CodeInfo.objects.get(scan_info=a_scan)
                scan_result = ScanResult.objects.get(code_info=code_info) 
            except:
                code_info = None
                scan_result = None
            local_scan = LocalScanInfo.objects.get(scan_info=a_scan) or None
            url_scan = None
            scan = Scan(a_scan, code_info, url_scan, local_scan, scan_result)
            serializer = ScanSerializer(scan)
            chromo.append(serializer.data)
        except:
            pass

for a in chromo:
    print a

