from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from services.geocoder.geocoding_service import GeocodingService

from .models import City
from .serializers import CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    geocoding_service = GeocodingService()

    def perform_create(self, serializer):
        city_name = serializer.validated_data['name']
        try:
            location = self.geocoding_service.get_location(city_name)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

        serializer.save(location=location)

    @action(detail=False, methods=['get'], url_path='nearest')
    def nearest_cities(self, request):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')

        if lat is None or lon is None:
            return Response({
                "error": "Please provide 'lat' and 'lon' as query parameters."},
                status=400)

        user_location = Point(float(lon), float(lat), srid=4326)
        cities = City.objects.annotate(
            distance=Distance('location', user_location)
        ).order_by('distance')[:2]

        serializer = self.get_serializer(cities, many=True)
        return Response(serializer.data)
