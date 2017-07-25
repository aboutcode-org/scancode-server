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

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Scan(models.Model):
    """
    Store various attributes of a scan
    """
    def __str__(self):
        return self.scan_type

    is_complete = models.BooleanField(default=False, help='True if the scan is completed by celery and result are stored')
    user = models.ForeignKey(User, blank=True, null=True, help='logged in user')
    url = models.URLField(max_length=2000, blank=True, null=True, help='url from where the code is fetched')
    scan_directory = models.CharField(max_length=200, help='directory or file in which the code is stored')
    scancode_notice = models.CharField(max_length=2000, blank=True, null=True, help='notice by the scancode-toolkit')
    scancode_version = models.CharField(max_length=200, blank=True, null=True, help='version of scancode being used')
    files_count = models.IntegerField(null=True, blank=True, default=0, help='number of files under scan')
    scan_start_time = models.DateTimeField(help='time at which scan starts', blank=True, null=True)
    scan_end_time = models.DateTimeField(help='time at which scan ends', blank=True, null=True)


class ScannedFile(models.Model):
    """
    Store path of every file being scanned
    """
    def __str__(self):
        return self.file_path

    scan = models.ForeignKey(Scan)
    file_path = models.CharField(max_length=400, help='path of file scanned')


class License(models.Model):
    """
    Represent a license as detected in a file
    """
    def __str__(self):
        return self.key

    scanned_file = models.ForeignKey(ScannedFile)
    category = models.CharField(max_length=1000, help='category of license')
    start_line = models.IntegerField(help='start line of license')
    end_line = models.IntegerField(help='end line of license in the file')
    spdx_url = models.URLField(max_length=2000, help='spdx url of license')
    text_url = models.URLField(max_length=2000, help='text url of license')
    spdx_license_key = models.CharField(max_length=200, help='spdx license key')
    homepage_url = models.URLField(max_length=2000, help='homepage url of license')
    score = models.IntegerField(help='score of license')
    key = models.CharField(max_length=200, help='key of license')
    owner = models.CharField(max_length=500, help='owner of the license')
    dejacode_url = models.URLField(max_length=2000, help='dejacode url of the license detected')
    matched_rule = JSONField(help='matched rule about the license detected')


class Copyright(models.Model):
    """
    Stores the copyright information present in the code
    """
    def __str__(self):
        return str(self.start_line)

    scanned_file = models.ForeignKey(ScannedFile)
    start_line = models.IntegerField(help='start line of the copyright')
    end_line = models.IntegerField(help='end line of the copyright')


class CopyrightHolder(models.Model):
    """
    Stores the information of the copyright holders of the code
    """
    def __str__(self):
        return self.holder

    copyright = models.ForeignKey(Copyright)
    holder = models.CharField(max_length=400, help='copyright holders of the copyright')


class CopyrightStatement(models.Model):
    """
    Stores the information of the copyright statements in the code
    """
    def __str__(self):
        return self.statement

    copyright = models.ForeignKey(Copyright)
    statement = models.CharField(max_length=500, help='copyright statements of the copyright')


class CopyrightAuthor(models.Model):
    """
    Stores the information of the copyright authors in the code
    """
    def __str__(self):
        return self.author

    copyright = models.ForeignKey(Copyright)
    author = models.CharField(max_length=200, help='copyright authors of the copyright')


class Package(models.Model):
    """
    Stores the package imformation present in the code
    """
    def __str__(self):
        return self.package

    scanned_file = models.ForeignKey(ScannedFile)
    package = JSONField(max_length=1000, help='information of the package')


class ScanError(models.Model):
    """
    Stores the errors generated during the scan
    """
    def __str__(self):
        return self.scan_error

    scanned_file = models.ForeignKey(ScannedFile)
    scan_error = models.CharField(max_length=1000, help='information about the scan errors')
