from decimal import Decimal
from random import randint

from provider.models.provider import Provider


def increase_customers_debt():
    customers = Provider.objects.exclude(provider=None)
    for customer in customers:
        random_amount = Decimal(randint(5, 500))
        customer.debt += random_amount
        customer.save()


def decrease_customers_debt():
    customers = Provider.objects.exclude(provider=None)
    for customer in customers:
        random_amount = Decimal(randint(100, 10000))
        customer.debt -= random_amount
        customer.save()


def clear_customers_debt(customer_ids: list[int]):
    customers = Provider.objects.filter(id__in=customer_ids)
    for customer in customers:
        customer.debt = 0
        customer.save()
