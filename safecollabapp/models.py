from django.db import models
from django.contrib.auth.models import User, Group

# Container class for users and messages and other stuff a user needs
class SafeCollabUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.BinaryField(editable = False)

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    encrypted = models.BooleanField(default = False)
    time = models.DateTimeField(auto_now_add = True) # timestamps upon message creation
    text = models.TextField() # actual text (plain or encrypted) of the message

#-----------------------------------------------------------------------------------------
# potential models and helper functions to generate paths for reports and documents
def report_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/instance.owner/instance.name
    return '{0}/{1}'.format(instance.owner, instance.name)

def datafile_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/instance.owner/instance.name
    return '{0}/{1}/{2}'.format(instance.report.name, instance.owner, instance.name)

# Create your models here.
class Report(models.Model):
    #name = models.CharField(max_length=128)
    #owner = models.CharField(max_length=128)
    #reportfile = models.FileField(upload_to=report_path)
    reportfile = models.FileField(upload_to='documents/%Y/%m/%d')

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

#-----------------------------------------------------------------------------------------
# temporary model used for file upload example
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
