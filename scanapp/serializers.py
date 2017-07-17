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
    scan_info_serializer = ScanInfoSerializer()
    class Meta:
        model = UserInfo
        exclude = ('id',)


class UrlScanInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `URLScanInfo` with all fields
    """
    scan_info = ScanInfoSerializer()
    class Meta:
        model = URLScanInfo
        exclude = ('id',)


class LocalScanInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `LocalScanInfo` with all fields
    """
    scan_info = ScanInfoSerializer()
    
    class Meta:
        model = LocalScanInfo
        exclude = ('id',)

class CodeInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CodeInfo` with all fields
    """
    scan_info = ScanInfoSerializer()
    class Meta:
        model = CodeInfo
        exclude = ('id',)

class ScanResultSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `ScanResult` with all fields
    """
    code_info = CodeInfoSerializer()
    class Meta:
        model = ScanResult
        exclude = ('id',)

class ScanFileInfoSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `ScanFileInfo` with all fields
    """
    scan_result = ScanResultSerializer()
    class Meta:
        model = ScanFileInfo
        exclude = ('id',)

class LicenseSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `License` with all fields
    """
    scan_file_info = ScanFileInfoSerializer()
    class Meta:
        model = License
        exclude = ('id',)

class MatchedRuleSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `MatchedRule` with all fields
    """
    license = LicenseSerializer()
    class Meta:
        model = MatchedRule
        exclude = ('id',)

class MatchedRuleLicenseSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `MatchedRuleLicense` with all fields
    """
    matched_rule = MatchedRuleSerializer()
    class Meta:
        model = MatchedRuleLicenses
        exclude = ('id',)

class CopyrightSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Copyright` with all fields
    """
    scan_file_info = ScanFileInfoSerializer()
    class Meta:
        model = Copyright
        exclude = ('id',)

class CopyrightHolderSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CopyrightHolders` with all fields
    """
    copyright = CopyrightSerializer()
    class Meta:
        model = CopyrightHolders
        exclude = ('id',)

class CopyrightStatementSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CopyrightHolders` with all fields
    """
    copyright = CopyrightSerializer()
    class Meta:
        model = CopyrightStatements
        exclude = ('id',)

class CopyrightAuthorSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CopyrightAuthor` with all fields
    """
    copyright = CopyrightSerializer()
    class Meta:
        model = CopyrightAuthor
        exclude = ('id',)

class PackageSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Package` with all fields
    """
    scan_file_info = ScanFileInfoSerializer()
    class Meta:
        model = Package
        exclude = ('id',)

class ScanErrorSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Package` with all fields
    """
    scan_file_info = ScanFileInfoSerializer()
    class Meta:
        model = ScanError
        exclude = ('id',)
