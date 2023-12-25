from decimal import Decimal
from unittest.mock import patch

import pytest
from tests.provider.factories import ProviderFactory, CustomerFactory, Provider

from provider.tasks import increase_debt_task, decrease_debt_task, clear_debt_task


@patch('provider.tasks.increase_debt_task.delay')
def test_mock_increase_debt_task(mock_delay):
    assert increase_debt_task.delay()
    mock_delay.assert_called_once()

    assert increase_debt_task.delay()
    mock_delay.assert_called()


@patch('provider.tasks.decrease_debt_task.delay')
def test_mock_decrease_debt_task(mock_delay):
    assert decrease_debt_task.delay()
    mock_delay.assert_called_once()

    assert decrease_debt_task.delay()
    mock_delay.assert_called()


@pytest.mark.django_db
@patch('provider.tasks.clear_debt_task.delay')
def test_mock_clear_debt_task(mock_delay):
    provider = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL, debt=Decimal('0.0'))
    customer1 = CustomerFactory(provider=provider, level=Provider.ProviderLevelChoices.SECOND_LEVEL)
    customer2 = CustomerFactory(provider=customer1, level=Provider.ProviderLevelChoices.THIRD_LEVEL)
    customer3 = CustomerFactory(provider=customer2, level=Provider.ProviderLevelChoices.FOURTH_LEVEL)
    CustomerFactory(provider=customer3, level=Provider.ProviderLevelChoices.FIFTH_LEVEL)
    customer_ids = list(Provider.objects.exclude(provider=None).values_list('id', flat=True))

    assert clear_debt_task.delay(customer_ids)
    mock_delay.assert_called_once()
    mock_delay.assert_called_with(customer_ids)
