from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

# Container class for users and messages and other stuff a user needs
class SafeCollabUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)