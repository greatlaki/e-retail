from decimal import Decimal

from django.db import transaction

from provider.constants import VALID_PROVIDER_LEVEL
from provider.models.product import Product, ProductToProvider
from provider.models.provider import Provider
from rest_framework import serializers

from provider.serializers.contact_serializers import ContactSerializer
from provider.serializers.product_serializers import ProductSerializer


class ProviderSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all(), read_only=False, required=False)
    debt = serializers.DecimalField(max_digits=32, decimal_places=2, default=Decimal('0.0'))
    level = serializers.ChoiceField(choices=Provider.ProviderLevelChoices.choices, required=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), read_only=False, required=False)

    contacts = ContactSerializer(read_only=True, many=True)
    retail_products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Provider
        fields = ('id', 'name', 'provider', 'debt', 'level', 'contacts', 'retail_products', 'product_id')

    @staticmethod
    def custom_validate_provider(level: Provider.ProviderLevelChoices):
        if level > Provider.ProviderLevelChoices.FIRST_LEVEL:
            raise serializers.ValidationError({'provider': 'Enter your provider'})

    @staticmethod
    def custom_validate_first_level_chain(level: Provider.ProviderLevelChoices, provider: Provider):
        if level == Provider.ProviderLevelChoices.FIRST_LEVEL and provider is not None:
            raise serializers.ValidationError({'level': 'Factory cannot have a provider'})

    @staticmethod
    def custom_validate_level_in_chain(level: Provider.ProviderLevelChoices, provider: Provider):
        if provider.level == Provider.ProviderLevelChoices.FIFTH_LEVEL:
            raise serializers.ValidationError({'provider': 'Invalid provider'})

        valid_level = provider.level + 1
        customers = provider.customers.all()
        if customers:
            for item in customers:
                if item.level == customers[0].level:
                    raise serializers.ValidationError(
                        {'provider': 'The selected provider is already involved in the chain.'}
                    )

        if level < provider.level:
            raise serializers.ValidationError({'provider': VALID_PROVIDER_LEVEL.format(valid_level=valid_level)})

        elif level == provider.level:
            raise serializers.ValidationError({'provider': VALID_PROVIDER_LEVEL.format(valid_level=valid_level)})

        elif level > provider.level + 1:
            raise serializers.ValidationError({'provider': VALID_PROVIDER_LEVEL.format(valid_level=valid_level)})

    @staticmethod
    def custom_validate_provider_name(name: str):
        if len(name) > 50:
            raise serializers.ValidationError({'name': 'Invalid name length'})

    def validate(self, attrs):
        provider = attrs.get('provider', None)
        level = attrs.get('level', None)
        name = attrs.get('name', None)

        if name is not None:
            is_provider_exists = Provider.objects.filter(name=attrs['name'])
            if is_provider_exists:
                raise serializers.ValidationError({'name': 'Provider already exists.'})

        if level is not None:
            if provider is None:
                self.custom_validate_provider(level)
                return attrs

            self.custom_validate_first_level_chain(attrs['level'], provider)
            self.custom_validate_level_in_chain(level, provider)
        return super().validate(attrs=attrs)

    def create(self, validated_data):
        product = validated_data.pop('product_id', None)
        if product is not None:
            with transaction.atomic():
                provider = super().create(validated_data)
                ProductToProvider.objects.create(provider=provider, product=product)
                return provider
        return super().create(validated_data)

    def update(self, instance, validated_data):
        debt = validated_data.get('debt', None)
        product = validated_data.pop('product_id', None)
        name = validated_data.pop('name', None)

        if name is not None:
            self.custom_validate_provider_name(name)

        if debt is not None:
            raise serializers.ValidationError({'debt': 'You cannot update this field'})

        if product is not None:
            with transaction.atomic():
                provider = super().update(instance, validated_data)
                ProductToProvider.objects.create(provider=provider, product=product)

        return super().update(instance, validated_data)


class ProviderStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'name', 'debt')
