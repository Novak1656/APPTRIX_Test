from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CryptocurrencyAPIViewSet


router = DefaultRouter()
router.register(r'crypto', CryptocurrencyAPIViewSet, basename='crypto')

urlpatterns = [
    path('', include(router.urls)),
]
