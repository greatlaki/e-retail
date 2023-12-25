from decimal import Decimal

import pytest
from tests.provider.factories import ProviderFactory, CustomerFactory, Provider
from provider.tasks import increase_debt_task, decrease_debt_task, clear_debt_task


@pytest.mark.django_db
def test_task():
    provider = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL, debt=Decimal('0.0'))
    customer1 = CustomerFactory(provider=provider, level=Provider.ProviderLevelChoices.SECOND_LEVEL)
    customer2 = CustomerFactory(provider=customer1, level=Provider.ProviderLevelChoices.THIRD_LEVEL)
    customer3 = CustomerFactory(provider=customer2, level=Provider.ProviderLevelChoices.FOURTH_LEVEL)
    CustomerFactory(provider=customer3, level=Provider.ProviderLevelChoices.FIFTH_LEVEL)

    assert increase_debt_task.delay()
    assert decrease_debt_task.delay()
    assert clear_debt_task.delay(
        customer_ids=list(Provider.objects.exclude(provider=None).values_list('id', flat=True))
    )
