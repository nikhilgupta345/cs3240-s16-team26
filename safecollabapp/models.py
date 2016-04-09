from django.db import models

def report_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/instance.owner/instance.name
    return '{0}/{1}'.format(instance.owner, instance.name)

def datafile_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/instance.owner/instance.name
    return '{0}/{1}/{2}'.format(instance.report.name, instance.owner, instance.name)


# Create your models here.
class Report(models.Model):
    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)

    upload = models.FileField(upload_to=report_path)
    print(report_path)

    def __str__(self):  # use __unicode__ for Python 2, use __str__ on Python 3
        return self.name

class DataFile(models.Model):
    report = models.ForeignKey(Report)
    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    encrypted = models.BooleanField()

    upload = models.FileField(upload_to=datafile_path)

    def __str__(self):  # use __unicode__ for Python 2, use __str__ on Python 3
        return self.name

