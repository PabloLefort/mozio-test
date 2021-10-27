from django.urls import include, path
from rest_framework import routers

from core.views import ProviderViewSet, ServiceAreaView


router = routers.DefaultRouter()
router.register(r'providers', ProviderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('availability', ServiceAreaView.as_view())
]
