from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

# Container class for users and messages and other stuff a user needs
class SafeCollabUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.BinaryField(editable = False)

class PrivateMessage(models.Model):
    sender = models.ForeignKey(SafeCollabUser, on_delete=models.CASCADE, related_name='+')
    recipient = models.ForeignKey(SafeCollabUser, on_delete=models.CASCADE, related_name='+')
    encrypted = models.BooleanField(default = False)
    time = models.DateTimeField(auto_now_add = True) # timestamps upon message creation
    text = models.TextField() # actual text (plain or encrypted) of the message
