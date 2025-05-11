from rest_framework import serializers
from .models import CounselingCenter

class CounselingCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselingCenter
        fields = ['id', 'region', 'name', 'category', 'address', 'phone', 'website', 'latitude', 'longitude']
