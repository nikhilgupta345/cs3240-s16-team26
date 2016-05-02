from rest_framework import serializers
from safecollabapp.models import *
from django.contrib.auth.models import User, Group

class RFile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = RFile

class Report_Serializer(serializers.ModelSerializer):
    files = RFile_Serializer(many=True, read_only=True)
    class Meta:
        model = Report
        fields = ('owner', 'folder_id', 'time', 'short_desc', 'long_desc', 'private', 'group', 'files')