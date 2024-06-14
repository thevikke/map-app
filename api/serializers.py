from rest_framework import serializers
from .models import PointOfInterest

class PointOfInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfInterest
        fields = ['id', 'name', 'description', 'location', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by']