# affiliate_system/serializers.py

from rest_framework import serializers
from dashboard.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'name', 'last_name', 'avatar', 'bio']
