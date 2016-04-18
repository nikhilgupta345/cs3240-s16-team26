from django.db import models
from django.contrib.auth.models import User, Group

# Container class for users and messages and other stuff a user needs
class SafeCollabUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.BinaryField(editable = False, default=None)

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    encrypted = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True) # timestamps upon message creation
    text = models.TextField() # actual text (plain or encrypted) of the message

class Folder(models.Model):
    name = models.CharField(max_length=128)
    folder = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class Report(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='+')
    time = models.DateTimeField(auto_now_add=True) # timestamp
    short_desc = models.CharField(max_length=120) # short description
    long_desc = models.TextField() # long description
    private = models.BooleanField(default=False)
    # files are handled in the RFile class

# helper functions to generate paths for reports and documents
def report_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/instance.owner/instance.name
    return '{0}/{1}'.format(instance.owner, instance.name)

def datafile_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/instance.owner/instance.name
    return '{0}/{1}/{2}'.format(instance.report.name, instance.owner, instance.name)

class RFile(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='+')
    docfile = models.FileField(upload_to=datafile_path)
    encrypted = models.BooleanField(default=False)

# temporary model used for file upload example
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
