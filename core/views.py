from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Provider
from .serializers import ProviderSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all().order_by('-id')
    serializer_class = ProviderSerializer

    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            provider = Provider.create(values=serializer.validated_data)
            return Response(serializer.__class__(provider).data, status=201)
        else:
            return Response({'errors': serializer.errors}, status=400)


class ServiceAreaView(APIView):

    def get(self, request, format=None):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        if lat is None or lng is None:
            return Response({'error': 'Both lat and lng must be provided'}, status=400)

        result = Provider.lookup_point(lat, lng)
        serializer = ProviderSerializer(result, many=True)
        return Response(serializer.data)
