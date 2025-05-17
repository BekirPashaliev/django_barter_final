from rest_framework import viewsets, permissions
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().select_related('user')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all().select_related('ad_sender', 'ad_receiver')
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs.filter(ad_sender__user=user) | qs.filter(ad_receiver__user=user)
