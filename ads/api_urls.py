from rest_framework import routers
from django.urls import path, include
from .viewsets import AdViewSet, ExchangeProposalViewSet

router = routers.DefaultRouter()
router.register(r'ads', AdViewSet)
router.register(r'proposals', ExchangeProposalViewSet)

urlpatterns = [path('', include(router.urls))]
