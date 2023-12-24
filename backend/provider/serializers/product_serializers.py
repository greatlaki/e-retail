from rest_framework import serializers
from provider.models.product import Product, ProductToProvider


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'model', 'first_date_of_release')


class ProductToProviderSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    provider_id = serializers.IntegerField(source='provider.id', read_only=True)

    class Meta:
        model = ProductToProvider
        fields = ('id', 'product_id', 'provider_id')
