from django.db import models
from django_extended.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=150)
    model = models.CharField(max_length=150)
    first_date_of_release = models.DateField(null=True, blank=True)

    providers = models.ForeignKey(
        'provider.Provider', on_delete=models.CASCADE, null=True, blank=True, related_name='products'
    )
