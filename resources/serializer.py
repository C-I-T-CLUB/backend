from rest_framework import serializers
from .models import Resource

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"
        # fields = ('file_id', 'file','unitname', 'year', 'course' , 'date_added')