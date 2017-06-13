from __future__ import unicode_literals

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.
class UserInfo(models.Model):
    def __str__(self):
        return self.user.username

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=0)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class AnonymousUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return 'guest-%s' % self.user.id


class CodeInfo(models.Model):
    def __str__(self):
        return self.url

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code_url_path = models.CharField(max_length=3000)
    code_file_number = models.IntegerField(null=True, blank=True)
    code_file_size = models.IntegerField(null=True, blank=True, default=0)


class ScannedResults(models.Model):
    def __str__(self):
        return self.total_errors

    code_info = models.ForeignKey(CodeInfo)
    scanned_json_result = JSONField()
    scanned_html_result = models.CharField(max_length=10000)
    scanned_files = models.IntegerField(null=True, blank=True, default=0)
    total_errors = models.IntegerField(null=True, blank=True, default=0)
    scan_time = models.IntegerField(null=True, blank=True, default=0)
    scan_info = models.CharField(max_length=3000)


class License(models.Model):
    def __str__(self):
        return self.license

    result_info = models.ForeignKey(ScannedResults)
    license = models.CharField(max_length=1000)


class Copyright(models.Model):
    def __str__(self):
        return self.copyright

    result_info = models.ForeignKey(ScannedResults)
    copyright = models.CharField(max_length=1000)


class Package(models.Model):
    def __str__(self):
        return self.package

    result_info = models.ForeignKey(ScannedResults)
    package = models.CharField(max_length=1000)
