from django.urls import include, path
from rest_framework import routers

from core.views import ProviderViewSet, ServiceAreaViewSet, AvailabilityView


provider_router = routers.DefaultRouter()
provider_router.register(r'provider', ProviderViewSet)

service_area_router = routers.DefaultRouter()
service_area_router.register(r'service-area', ServiceAreaViewSet)


urlpatterns = [
    path('', include(provider_router.urls)),
    path('', include(service_area_router.urls)),
    path('availability', AvailabilityView.as_view())
]
