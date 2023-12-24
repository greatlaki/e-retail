from decimal import Decimal

import pytest

from tests.provider.factories import (
    ProviderFactory,
    ContactFactory,
    ProductFactory,
    Provider,
    CustomerFactory,
    ProductToProviderFactory,
)


class TestGet:
    @pytest.mark.django_db
    def test_get_provider(self, api_client):
        provider = ProviderFactory(name='First level', provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        ContactFactory(city='Minsk', provider=provider)
        ContactFactory(city='Grodno', provider=provider)
        product = ProductFactory(name='Product')
        ProductToProviderFactory(product=product, provider=provider)

        response = api_client.get(f'/api/providers/{provider.pk}/')

        assert response.status_code == 200


class TestPatch:
    @pytest.mark.django_db
    def test_it_updates_provider(self, api_client):
        provider = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        data = {'name': 'test provider'}

        response = api_client.patch(f'/api/providers/{provider.pk}/', data=data, format='json')

        provider.refresh_from_db()
        assert response.status_code == 200
        assert response.data['name'] == provider.name

    @pytest.mark.django_db
    def test_it_returns_error_if_update_debt(self, api_client):
        provider = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        data = {'debt': Decimal('0.0')}

        response = api_client.patch(f'/api/providers/{provider.pk}/', data=data, format='json')

        provider.refresh_from_db()
        assert response.status_code == 400
        assert response.data['debt'] == 'You cannot update this field'

    @pytest.mark.django_db
    def test_it_returns_error_if_provider_did_not_selected(self, api_client):
        provider_1 = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        CustomerFactory(provider=provider_1, level=Provider.ProviderLevelChoices.SECOND_LEVEL)

        provider_3 = CustomerFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_4 = CustomerFactory(provider=provider_3, level=Provider.ProviderLevelChoices.SECOND_LEVEL)
        provider_5 = CustomerFactory(provider=provider_4, level=Provider.ProviderLevelChoices.THIRD_LEVEL)
        data = {'level': Provider.ProviderLevelChoices.SECOND_LEVEL}

        response = api_client.patch(f'/api/providers/{provider_5.pk}/', data=data, format='json')

        provider_5.refresh_from_db()
        assert response.status_code == 400
        assert response.data['provider'] == ['Enter your provider']

    @pytest.mark.django_db
    def test_it_returns_error_if(self, api_client):
        provider_1 = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        CustomerFactory(provider=provider_1, level=Provider.ProviderLevelChoices.SECOND_LEVEL)

        provider_3 = CustomerFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_4 = CustomerFactory(provider=provider_3, level=Provider.ProviderLevelChoices.SECOND_LEVEL)
        provider_5 = CustomerFactory(provider=provider_4, level=Provider.ProviderLevelChoices.THIRD_LEVEL)
        data = {'provider': provider_1.pk, 'level': Provider.ProviderLevelChoices.SECOND_LEVEL}

        response = api_client.patch(f'/api/providers/{provider_5.pk}/', data=data, format='json')

        provider_5.refresh_from_db()
        assert response.status_code == 400
        assert response.data['provider'] == ['The selected provider is already involved in the chain.']


class TestDelete:
    @pytest.mark.django_db
    def test_it_deletes_provider(self, api_client):
        provider_1 = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)

        response = api_client.delete(f'/api/providers/{provider_1.pk}/')

        assert response.status_code == 204
