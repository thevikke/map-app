from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import PointOfInterest

class PointOfInterestSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = PointOfInterest
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'created_at', 'created_by', 'owner']
        read_only_fields = ['created_at', 'created_by']

    def get_latitude(self, obj):
        return obj.location.y

    def get_longitude(self, obj):
        return obj.location.x

    def create(self, validated_data):
        latitude = self.context['request'].data.get('latitude')
        longitude = self.context['request'].data.get('longitude')
        location = Point(float(longitude), float(latitude), srid=4326)
        validated_data['location'] = location
        return super().create(validated_data)