from django.db import models
from django_extended.models import BaseModel
from provider.models.provider import Provider


class Product(BaseModel):
    name = models.CharField(max_length=150)
    model = models.CharField(max_length=150)
    first_date_of_release = models.DateField(null=True, blank=True)

    product_for = models.ManyToManyField(Provider, through='ProductToProvider')

    def __str__(self):
        return f'{self.name}: {self.model}'

    class Meta:
        db_table = 'products'


class ProductToProvider(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='providers')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='products')

    class Meta:
        db_table = 'products_to_providers'
        unique_together = ('product', 'provider')
