from drf_spectacular.utils import extend_schema
from rest_framework import generics
from provider.models.provider import Provider
from provider.serializers.provider_serializers import ProviderListCreateSerializer


@extend_schema(tags=['Provider'])
class ProviderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProviderListCreateSerializer
    queryset = Provider.objects.all()
