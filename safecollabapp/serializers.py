from rest_framework import serializers
from safecollabapp.models import *

class RFile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = RFile

class Report_Serializer(serializers.ModelSerializer):
    files = RFile_Serializer(many=True, read_only=True)
    class Meta:
        model = Report
        fields = ('owner', 'time', 'short_desc', 'long_desc', 'private', 'files')