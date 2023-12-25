from datetime import datetime
from django.utils import timezone

from rest_framework import serializers

from provider.models.product import Product, ProductToProvider


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'model', 'first_date_of_release')

    @staticmethod
    def custom_validate_product_name(name: str):
        if len(name) > 25:
            raise serializers.ValidationError({'name': 'Invalid name length'})

    @staticmethod
    def custom_validate_first_date_of_release(date: datetime):
        if date > timezone.now().date():
            raise serializers.ValidationError({'date': 'The release date of the product cannot be in the future.'})
        return date

    def update(self, instance, validated_data):
        name = validated_data.pop('name', None)
        first_date_of_release = validated_data.pop('first_date_of_release', None)

        if name is not None:
            self.custom_validate_product_name(name)
        if first_date_of_release is not None:
            self.custom_validate_first_date_of_release(first_date_of_release)

        return super().update(instance, validated_data)


class ProductToProviderSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    provider_id = serializers.IntegerField(source='provider.id', read_only=True)

    class Meta:
        model = ProductToProvider
        fields = ('id', 'product_id', 'provider_id')
