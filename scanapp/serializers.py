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
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `User` model
    """
    class Meta:
        model = User
        fields = '__all__'

class UserInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `UserInfo` model with all field
    """
    user = UserSerializer()
    scan_info_serializer = ScanInfoSerializer()
    class Meta:
        model = UserInfo
        fields = '__all__'

class UrlScanInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `URLScanInfo` with all fields
    """
    scan_info = ScanInfoSerializer()
    class Meta:
        model = URLScanInfo
        fields = '__all__'

class LocalScanInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `LocalScanInfo` with all fields
    """
    scan_info = ScanInfoSerializer()
    class Meta:
        model = LocalScanInfo
        fields = '__all__'

class CodeInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CodeInfo` with all fields
    """
    scan_info = ScanInfoSerializer()
    class Meta:
        model = CodeInfo
        fields = '__all__'

class ScanResultSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `ScanResult` with all fields
    """
    code_info = CodeInfoSerializer()
    class Meta:
        model = ScanResult
        fields = '__all__'

class ScanFileInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `ScanFileInfo` with all fields
    """
    scan_result = ScanResultSerializer()
    class Meta:
        model = ScanFileInfo
        fields = '__all__'

class LicenseSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `License` with all fields
    """
    scan_file_info = ScanFileInfoSerializer()
    class Meta:
        model = License
        fields = '__all__'

class MatchedRuleSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `MatchedRule` with all fields
    """
    license = LicenseSerializer()
    class Meta:
        model = MatchedRule
        fields = '__all__'

class MatchedRuleLicenseSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `MatchedRuleLicense` with all fields
    """
    license = MatchedRuleSerializer()
    class Meta:
        model = MatchedRuleLicenses
        fields = '__all__'

class CopyrightSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Copyright` with all fields
    """
    scan_file_info = ScanFileInfoSerializer()
    class Meta:
        model = Copyright
        fields = '__all__'

class CopyrightHolderSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CopyrightHolders` with all fields
    """
    copyright = CopyrightSerializer()
    class Meta:
        model = CopyrightHolders
        fields = '__all__'

class CopyrightStatementSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CopyrightHolders` with all fields
    """
    copyright = CopyrightSerializer()
    class Meta:
        model = CopyrightStatements
        fields = '__all__'

class CopyrightAuthorSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CopyrightAuthor` with all fields
    """
    copyright = CopyrightSerializer()
    class Meta:
        model = CopyrightAuthor
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Package` with all fields
    """
    scan_file_info = ScanFileInfoSerializer()
    class Meta:
        model = Package
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Package` with all fields
    """
    scan_file_info = ScanFileInfoSerializer()
    class Meta:
        model = ScanError
        fields = '__all__'

class AllModelSerializer(serializers.BaseSerializer):
    """
    Base serializer to combine all the serializers
    """
    scan_info = ScanInfoSerializer()
    user_info = UserInfoSerializer()
    url_scan_info = UrlScanInfoSerializer()
    local_scan_info = LocalScanInfoSerializer()

