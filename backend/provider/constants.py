from django.db import models


class ProviderTypeChoices(models.TextChoices):
    FACTORY = 'FACTORY'
    DISTRIBUTOR = 'DISTRIBUTOR'
    DEALERSHIP = 'DEALERSHIP'
    LARGE_RETAIL = 'LARGE_RETAIL'
    INDIVIDUAL_ENTREPRENEUR = 'INDIVIDUAL_ENTREPRENEUR'
