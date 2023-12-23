from decimal import Decimal

from provider.constants import VALID_PROVIDER_LEVEL
from provider.models.provider import Provider
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ProviderListCreateSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all(), read_only=False, required=False)
    debt = serializers.DecimalField(max_digits=32, decimal_places=2, default=Decimal('0.0'))
    level = serializers.ChoiceField(choices=Provider.ProviderLevelChoices.choices, required=True)

    class Meta:
        model = Provider
        fields = ('id', 'name', 'provider', 'debt', 'level')

    @staticmethod
    def custom_validate_provider(level: Provider.ProviderLevelChoices):
        if level > Provider.ProviderLevelChoices.FIRST_LEVEL:
            raise serializers.ValidationError({'provider': 'Enter your provider'})

    @staticmethod
    def custom_validate_first_level_chain(level: Provider.ProviderLevelChoices, provider: Provider):
        if level == Provider.ProviderLevelChoices.FIRST_LEVEL and provider is not None:
            raise ValidationError({'level': 'Factory cannot have a provider'})

    @staticmethod
    def custom_validate_level_in_chain(level: Provider.ProviderLevelChoices, provider: Provider):
        if provider.level == Provider.ProviderLevelChoices.FIFTH_LEVEL:
            raise ValidationError({'provider': 'Invalid provider'})

        valid_level = provider.level + 1
        customers = provider.customers.all()
        if customers:
            for item in customers:
                if item.level == customers[0].level:
                    raise ValidationError({'provider': 'The selected provider is already involved in the chain.'})

        if level < provider.level:
            raise ValidationError({'provider': VALID_PROVIDER_LEVEL.format(valid_level=valid_level)})

        if level == provider.level:
            raise ValidationError({'provider': VALID_PROVIDER_LEVEL.format(valid_level=valid_level)})

        if level > provider.level + 1:
            raise ValidationError({'provider': VALID_PROVIDER_LEVEL.format(valid_level=valid_level)})

    def validate(self, attrs):
        provider = attrs.get('provider', None)
        level = attrs['level']

        is_provider_exists = Provider.objects.filter(name=attrs['name'])
        if is_provider_exists:
            raise serializers.ValidationError({'name': 'Provider already exists.'})

        if provider is None:
            self.custom_validate_provider(level)
            return attrs

        self.custom_validate_first_level_chain(attrs['level'], provider)
        self.custom_validate_level_in_chain(level, provider)
        return attrs
