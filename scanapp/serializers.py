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

from django.contrib.auth.models import User

from rest_framework import serializers

from scanapp.models import Copyright
from scanapp.models import CopyrightAuthor
from scanapp.models import CopyrightHolder
from scanapp.models import CopyrightStatement
from scanapp.models import License
from scanapp.models import Package
from scanapp.models import Scan
from scanapp.models import ScanError
from scanapp.models import ScannedFile


class ScanSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Scan` model with all fields excluding `id`
    """
    class Meta:
        model = Scan
        exclude = ('id',)


class ScannedFileSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `ScannedFile` with all fields excluding `id` and `scan`
    """
    class Meta:
        model = ScannedFile
        exclude = ('id', 'scan')


class LicenseSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `License` with all fields excluding `id` and `scanned_file`
    """
    class Meta:
        model = License
        exclude = ('id', 'scanned_file')


class CopyrightSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Copyright` with all fields excluding `id` and `scanned_file`
    """
    class Meta:
        model = Copyright
        exclude = ('id', 'scanned_file')


class CopyrightHolderSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CopyrightHolders` with all fields excluding `id` and `copyright`
    """
    class Meta:
        model = CopyrightHolder
        exclude = ('id', 'copyright')


class CopyrightStatementSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CopyrightHolders` with all fields excluding `id` and `copyright`
    """
    class Meta:
        model = CopyrightStatement
        exclude = ('id', 'copyright')


class CopyrightAuthorSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `CopyrightAuthor` with all fields excluding `id` and `copyright`
    """
    class Meta:
        model = CopyrightAuthor
        exclude = ('id', 'copyright')


class PackageSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Package` with all fields excluding `id` and `scanned_file`
    """
    class Meta:
        model = Package
        exclude = ('id', 'scanned_file')


class ScanErrorSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for `Package` with all fields excluding `id` and `scanned_file`
    """
    class Meta:
        model = ScanError
        exclude = ('id', 'scanned_file')


class AllModelSerializer(serializers.Serializer):
    """
    A single serializer that takes care of all the Model Serializers and bind them together
    """
    scan = ScanSerializer()
    scanned_file = ScannedFileSerializer(many=True)
    license = LicenseSerializer(many=True)
    copyright = CopyrightSerializer(many=True)
    copyright_holder = CopyrightHolderSerializer(many=True)
    copyright_statement = CopyrightStatementSerializer(many=True)
    copyright_author = CopyrightAuthorSerializer(many=True)
    package = PackageSerializer(many=True)
    scan_error = ScanErrorSerializer(many=True)


class AllModelSerializerHelper(object):
    """
    Receive Scan Instance as `scan` and creates objects of all the other models
    """

    def __init__(self, scan):
        self.scan = scan
        self.scanned_file = ScannedFile.objects.filter(scan=self.scan)
        self.license = License.objects.filter(scanned_file__in=(self.scanned_file))
        self.copyright = Copyright.objects.filter(scanned_file__in=(self.scanned_file))
        self.copyright_holder = CopyrightHolder.objects.filter(copyright__in=(self.copyright))
        self.copyright_statement = CopyrightStatement.objects.filter(copyright__in=(self.copyright))
        self.copyright_author = CopyrightAuthor.objects.filter(copyright__in=(self.copyright))
        self.package = Package.objects.filter(scanned_file__in=(self.scanned_file))
        self.scan_error = ScanError.objects.filter(scanned_file__in=(self.scanned_file))
