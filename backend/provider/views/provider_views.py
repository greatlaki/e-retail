from rest_framework import generics
from provider.models.provider import Provider
from provider.serializers.provider_serializers import ProviderListCreateSerializer


class ProviderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProviderListCreateSerializer
    queryset = Provider.objects.all()
