from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema
from rest_framework import generics

from provider.filters import ProviderFilterSet
from provider.models.provider import Provider
from provider.serializers.provider_serializers import ProviderSerializer, ProviderStatisticSerializer


@extend_schema(tags=['Provider'])
class ProviderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProviderFilterSet


@extend_schema(tags=['Provider'])
class ProviderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return


@extend_schema(tags=['Provider'])
class ProviderStatisticAPIView(generics.ListAPIView):
    serializer_class = ProviderStatisticSerializer

    def get_queryset(self):
        average_debt = Provider.objects.aggregate(avg_debt=Avg('debt'))['avg_debt']
        return Provider.objects.filter(debt__gt=average_debt)
