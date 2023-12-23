from rest_framework import serializers
from provider.models.product import Product
from provider.models.provider import Provider


class ProductListCreateSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'model', 'first_date_of_release', 'provider')
