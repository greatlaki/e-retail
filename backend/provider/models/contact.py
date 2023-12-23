from django.db import models
from django_extended.models import BaseModel


class Contact(BaseModel):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    street = models.CharField(max_length=150)
    house_no = models.CharField(max_length=150)

    provider = models.ForeignKey(
        'provider.Provider', on_delete=models.CASCADE, null=True, blank=True, related_name='contacts'
    )

    def __str__(self):
        return f'{self.email}: {self.city}, {self.street}, {self.house_no}'
