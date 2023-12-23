from provider.models.provider import Provider
from rest_framework import serializers


class ProviderListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'
