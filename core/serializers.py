from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.error import GEOSException

from .models import Provider, ServiceArea


class ServiceAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceArea
        fields = '__all__'

    def validate_poly(self, value):
        try:
            dot = GEOSGeometry(f'POLYGON (({value}))', srid=4326)
            return dot
        except GEOSException:
            raise serializers.ValidationError('Invalid Polygon Area')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # clean SRID and POLYGON strings from PolygonField
        rep['poly'] = rep['poly'].split('((')[1].replace('))', '')
        return rep


class ProviderSerializer(serializers.ModelSerializer):
    areas = ServiceAreaSerializer(required=True, many=True)

    class Meta:
        model = Provider
        fields = '__all__'
