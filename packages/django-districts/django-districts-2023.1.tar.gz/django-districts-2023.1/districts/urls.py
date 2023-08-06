from django.urls import path, include
from rest_framework.routers import DefaultRouter

from districts.views import *

router = DefaultRouter()
router.register(r'region', Regions_ViewSet, basename='Regions_ViewSet')
router.register(r'district', Districts_ViewSet, basename='Districts_ViewSet')
router.register(r'county', County_ViewSet, basename='County_ViewSet')
router.register(r'subcounty', SubCounty_ViewSet, basename='SubCounty_ViewSet')
router.register(r'parish', Parish_ViewSet, basename='Parish_ViewSet')
router.register(r'location', Location_ViewSet, basename='Location_ViewSet')

urlpatterns = [
    path('', include(router.urls)),
]