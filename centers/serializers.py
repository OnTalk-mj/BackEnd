from rest_framework import serializers
from .models import CounselingCenter

class CounselingCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselingCenter
        fields = ['id', 'name', 'region', 'category', 'phone', 'address', 'latitude', 'longitude']
