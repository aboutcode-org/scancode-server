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
    Store various attributes of a scan like `scan_type`, `is_complete`, `user`, 
    `URL`, `code_directory`, `total_code_files`, `code_size`, `scancode_notice`,
    `scancode_version`, `files_count`, `total_error`, `scan_time`
    """
    def __str__(self):
        return self.scan_type

    scan_types = (
        ('url', 'url'),
        ('localscan', 'localscan'),
    )

    scan_type = models.CharField(max_length=20, choices=scan_types, default='url')
    is_complete = models.BooleanField(default=False)
    user = models.ForeignKey(User, blank=True, null=True)
    URL = models.URLField(max_length=2000, blank=True, null=True)
    scan_directory = models.CharField(max_length=200)
    total_code_files = models.IntegerField(null=True, blank=True)
    code_size = models.IntegerField(null=True, blank=True, default=0)
    scancode_notice = models.CharField(max_length=2000, blank=True, null=True)
    scancode_version = models.CharField(max_length=200, blank=True, null=True)
    files_count = models.IntegerField(null=True, blank=True, default=0)
    total_errors = models.IntegerField(null=True, blank=True, default=0)
    scan_time = models.IntegerField(null=True, blank=True, default=0)


class ScanFileInfo(models.Model):
    """
    Store path of every file being scanned
    """
    def __str__(self):
        return self.file_path

    scan = models.ForeignKey(Scan)
    file_path = models.CharField(max_length=400)


class License(models.Model):
    """
    Stores the License information present in the code
    """
    def __str__(self):
        return self.key

    scan_file_info = models.ForeignKey(ScanFileInfo)
    category = models.CharField(max_length=1000)
    start_line = models.IntegerField()
    spdx_url = models.URLField(max_length=2000)
    text_url = models.URLField(max_length=2000)
    spdx_license_key = models.CharField(max_length=200)
    homepage_url = models.URLField(max_length=2000)
    score = models.IntegerField()
    end_line = models.IntegerField()
    key = models.CharField(max_length=200)
    owner = models.CharField(max_length=500)
    dejacode_url = models.URLField(max_length=2000)


class MatchedRule(models.Model):
    """
    Stores the MatchedRule about License present in the code
    """
    def __str__(self):
        return str(self.matched_rule)

    license = models.ForeignKey(License)
    matched_rule = models.JSONField()


class Copyright(models.Model):
    """
    Stores the copyright information present in the code
    """
    def __str__(self):
        return str(self.start_line)

    scan_file_info = models.ForeignKey(ScanFileInfo)
    start_line = models.IntegerField()
    end_line = models.IntegerField()


class CopyrightHolder(models.Model):
    """
    Stores the information of the copyright holders of the code
    """
    def __str__(self):
        return self.holder

    copyright = models.ForeignKey(Copyright)
    holder = models.CharField(max_length=400)


class CopyrightStatement(models.Model):
    """
    Stores the information of the copyright statements in the code
    """
    def __str__(self):
        return self.statement

    copyright = models.ForeignKey(Copyright)
    statement = models.CharField(max_length=500)


class CopyrightAuthor(models.Model):
    """
    Stores the information of the copyright authors in the code
    """
    def __str__(self):
        return self.author

    copyright = models.ForeignKey(Copyright)
    author = models.CharField(max_length=200)


class Package(models.Model):
    """
    Stores the package imformation present in the code
    """
    def __str__(self):
        return self.package

    scan_file_info = models.ForeignKey(ScanFileInfo)
    package = models.JSONField(max_length=1000)


class ScanError(models.Model):
    """
    Stores the errors generated during the scan
    """
    def __str__(self):
        return self.scan_error

    scan_file_info = models.ForeignKey(ScanFileInfo)
    scan_error = models.CharField(max_length=1000)
