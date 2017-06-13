from django.db import models


# Give a scan Id to the every scan
# Associate the Id with the type of the scan
# There are two types of scans 'URL' or 'LocalScan'
class scanType(models.Model):
    scanId = models.AutoField(
        primary_key=True,
        verbose_name='Scan ID',
    )
    scantypes = (
        ('URL', 'URL'),
        ('Local Scan', 'localscan'),
    )
    scanType = models.CharField(
        max_length=15,
        choices=scantypes,
        default='URL'
    )


# Associate the type of user who applied the scan command to scanId
class scanApplier(models.Model):
    scanId = models.ForeignKey(
        scanType,
        db_column='scanId',
        on_delete=models.CASCADE,
    )
    Applier = (
        ('user', 'user'),
        ('guest', 'guest'),
    )
    Applier = models.CharField(
        max_length=10,
        choices=Applier,
        default='user'
    )


# Associate the scanId with an URL
class urlAttribute(models.Model):
    scanId = models.ForeignKey(
        scanType,
        db_column='scanId',
        on_delete=models.CASCADE,
    )
    URL = models.URLField(
        max_length=200,
    )


# Associate folder Name with the scanId
class localAttribute(models.Model):
    scanId = models.ForeignKey(
        scanType,
        db_column='scanId',
        on_delete=models.CASCADE,
    )
    folderName = models.CharField(
        max_length=200,
    )


# Associate other attributes of codebase to the scanId
class codeBaseAttributes(models.Model):
    scanId = models.ForeignKey(
        scanType,
        db_column='scanId',
        on_delete=models.CASCADE,
    )
    codeBaseSize = models.IntegerField(
        null=True,
        blank=True,
        default=0,
    )
    total_files = models.IntegerField(
        null=True,
        default=0,
    )


class codeBaseResults(models.Model):
    scanId = models.ForeignKey(
        scanType,
        db_column='scanId',
        on_delete=models.CASCADE,
    )
    fileId = models.AutoField(
        primary_key=True,
    )
    fileName = models.CharField(
        max_length=200,
    )
    filePath = models.CharField(
        max_length=200,
    )
    scanError = models.CharField(
        max_length=200,
    )


class licences(models.Model):
    fileId = models.ForeignKey(
        codeBaseResults,
        db_column='fileId',
    )
    licence = models.CharField(
        max_length=200,
    )


class copyrights(models.Model):
    fileId = models.ForeignKey(
        codeBaseResults,
        db_column='fileId',
    )
    copyright = models.CharField(
        max_length=200,
    )


class package(models.Model):
    fileId = models.ForeignKey(
        codeBaseResults,
        db_column='fileId',
    )
    packages = models.CharField(
        max_length=200,
    )
