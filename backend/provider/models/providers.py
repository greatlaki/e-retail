from decimal import Decimal
from django.db import models
from django_extended.models import BaseModel
from provider.constants import ProviderTypeChoices


class Provider(BaseModel):
    name = models.CharField(max_length=255)
    provider = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='supplier')
    debt = models.DecimalField(max_digits=32, decimal_places=2, default=Decimal('0.0'))
    type = models.CharField(max_length=35, choices=ProviderTypeChoices.choices, default=ProviderTypeChoices.FACTORY)

    def __str__(self):
        return self.name
