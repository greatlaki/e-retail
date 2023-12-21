from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django_extended.models import BaseModel
from provider.constants import VALID_PROVIDER_LEVEL


class Provider(BaseModel):
    class ProviderLevelChoices(models.IntegerChoices):
        FIRST_LEVEL = 0
        SECOND_LEVEL = 1
        THIRD_LEVEL = 2
        FOURTH_LEVEL = 3
        FIFTH_LEVEL = 4

    name = models.CharField(max_length=255)
    provider = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='supplier')
    debt = models.DecimalField(max_digits=32, decimal_places=2, default=Decimal('0.0'))
    level = models.IntegerField(choices=ProviderLevelChoices.choices, default=ProviderLevelChoices.FIRST_LEVEL)

    def __str__(self):
        return self.name

    def _validate_first_level_chain(self):
        if self.level == Provider.ProviderLevelChoices.FIRST_LEVEL:
            raise ValidationError('Factory cannot have a provider')

    def _validate_provider(self):
        if self.level > Provider.ProviderLevelChoices.FIRST_LEVEL and self.provider is None:
            raise ValidationError('Enter your provider')

    def _validate_level_in_chain(self):
        valid_level = Provider.ProviderLevelChoices(self.provider.level + 1).name

        if self.level < self.provider.level:
            raise ValidationError(VALID_PROVIDER_LEVEL.format(valid_level=valid_level))

        if self.level == self.provider.level:
            raise ValidationError(VALID_PROVIDER_LEVEL.format(valid_level=valid_level))

        if self.level > self.provider.level + 1:
            raise ValidationError(VALID_PROVIDER_LEVEL.format(valid_level=valid_level))

        if self.provider.supplier.all():
            raise ValidationError('The selected provider is already involved in the chain')

    def clean(self):
        self._validate_provider()
        if self.provider is not None:
            self._validate_first_level_chain()
            self._validate_level_in_chain()

    def save(self, force_insert: bool = False, force_update: bool = False, using=None, update_fields=None):
        return super().save(force_insert, force_update, using, update_fields)
