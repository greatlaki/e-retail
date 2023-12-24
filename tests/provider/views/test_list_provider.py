from decimal import Decimal

import pytest

from provider.models.provider import Provider
from tests.provider.factories import (
    ProviderFactory,
    CustomerFactory,
    ContactFactory,
    ProductFactory,
    ProductToProviderFactory,
)


@pytest.mark.django_db
class TestGet:
    def test_get_providers(self, api_client):
        provider_1 = ProviderFactory(name='First level', provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_2 = CustomerFactory(
            name='Second level', provider=provider_1, level=Provider.ProviderLevelChoices.SECOND_LEVEL
        )
        provider_3 = CustomerFactory(
            name='Third level', provider=provider_2, level=Provider.ProviderLevelChoices.THIRD_LEVEL
        )
        CustomerFactory(name='Fourth level', provider=provider_3, level=Provider.ProviderLevelChoices.FOURTH_LEVEL)

        response = api_client.get('/api/providers/')

        assert response.status_code == 200

    def test_get_providers_with_contacts_and_products(self, api_client):
        provider_1 = ProviderFactory(name='First level', provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_2 = CustomerFactory(
            name='Second level', provider=provider_1, level=Provider.ProviderLevelChoices.SECOND_LEVEL
        )
        ContactFactory(city='Minsk', provider=provider_1)
        ContactFactory(city='Grodno', provider=provider_1)
        ContactFactory(city='Brest', provider=provider_2)

        product1 = ProductFactory(name='Product')
        product2 = ProductFactory(name='Another Product')

        ProductToProviderFactory(product_id=product1, provider_id=provider_1)
        ProductToProviderFactory(product_id=product2, provider_id=provider_2)

        response = api_client.get('/api/providers/')

        assert response.status_code == 200

    def test_filter_by_country(self, api_client):
        provider_1 = ProviderFactory(name='First', provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_2 = ProviderFactory(name='Second', provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_3 = ProviderFactory(name='Third', provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_4 = ProviderFactory(name='Fourth', provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_5 = ProviderFactory(name='Fifth', provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)

        ContactFactory(country='Belarus', provider=provider_1)
        ContactFactory(country='Belarus', provider=provider_2)
        ContactFactory(country='Poland', provider=provider_3)
        ContactFactory(country='France', provider=provider_4)
        ContactFactory(country='England', provider=provider_5)

        response = api_client.get('/api/providers/?country=Belarus')

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_filter_by_product_ids(self, api_client):
        provider_1 = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_2 = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_3 = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_4 = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_5 = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)

        product1 = ProductFactory()
        product2 = ProductFactory()
        product3 = ProductFactory()

        ProductToProviderFactory(product_id=product1, provider_id=provider_1)
        ProductToProviderFactory(product_id=product1, provider_id=provider_2)
        ProductToProviderFactory(product_id=product1, provider_id=provider_3)

        ProductToProviderFactory(product_id=product2, provider_id=provider_5)
        ProductToProviderFactory(product_id=product2, provider_id=provider_4)

        ProductToProviderFactory(product_id=product3, provider_id=provider_1)
        ProductToProviderFactory(product_id=product3, provider_id=provider_3)

        response = api_client.get(f'/api/providers/?product_ids={product3.pk},{product2.pk}')

        assert response.status_code == 200
        assert len(response.data) == 4

    def test_it_returns_debt_statistic(self, api_client):
        provider_1 = ProviderFactory(
            provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL, debt=Decimal('0.0')
        )
        provider_2 = CustomerFactory(
            provider=provider_1, level=Provider.ProviderLevelChoices.SECOND_LEVEL, debt=Decimal('50.00')
        )
        provider_3 = CustomerFactory(
            provider=provider_2, level=Provider.ProviderLevelChoices.THIRD_LEVEL, debt=Decimal('50.00')
        )
        provider_4 = CustomerFactory(
            provider=provider_3, level=Provider.ProviderLevelChoices.FOURTH_LEVEL, debt=Decimal('50.00')
        )
        CustomerFactory(provider=provider_4, level=Provider.ProviderLevelChoices.FIFTH_LEVEL, debt=Decimal('50.00'))

        provider = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL, debt=Decimal('0.0'))
        provider_with_giant_debt = CustomerFactory(
            provider=provider, level=Provider.ProviderLevelChoices.SECOND_LEVEL, debt=Decimal('1000.00')
        )

        response = api_client.get('/api/providers/debt-statistic/')

        assert response.status_code == 200
        assert len(response.data) == 1
        assert Decimal(response.data[0]['debt']) == provider_with_giant_debt.debt
