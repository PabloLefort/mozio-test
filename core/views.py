from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Provider
from .serializers import ProviderSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    """
    Enables **Provider** CRUD operations.

    ###Attributes:
    - name
    - phone_number
    - email
    - language
    - currency
    - areas: list of ServiceArea's

    > In order to seek Providers given latitude and longitude see the Availability Service
    """
    queryset = Provider.objects.filter(deleted=False).order_by('-id')
    serializer_class = ProviderSerializer
    # NOTE: authentication should be for Mozio's admins
    permission_classes = [AllowAny]

    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            provider = Provider.create(values=serializer.validated_data)
            return Response(serializer.__class__(provider).data, status=201)
        else:
            return Response({'error': serializer.errors}, status=400)

    def destroy(self, request, pk=None):
        if Provider.delete(pk=pk):
            return Response({}, status=200)
        else:
            return Response({'error': 'Invalid provider id'}, status=404)


class ServiceAreaView(APIView):
    """
    Enables the possibility to retrieve Providers that are on the given latitude and longitude.

    ###Example:
    ```sh
    curl localhost:8000/availability?lat=-72.2804556&lng=42.9293281
    ```
    """

    def get(self, request, format=None):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        if lat is None or lng is None:
            return Response({'error': 'Both lat and lng must be provided'}, status=400)

        result = Provider.lookup_point(lat, lng)
        serializer = ProviderSerializer(result, many=True)
        return Response(serializer.data)
