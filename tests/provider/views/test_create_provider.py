import pytest
from provider.models.provider import Provider
from tests.provider.factories import ProviderFactory, CustomerFactory


@pytest.mark.django_db
class TestPost:
    def test_it_creates_first_level_in_retail_chain(self, api_client):
        provider = ProviderFactory.build(provider=None)
        data = {
            'name': provider.name,
            'level': Provider.ProviderLevelChoices.FIRST_LEVEL,
        }

        response = api_client.post('/api/providers/', data=data, format='json')

        assert response.status_code == 201
        assert response.data['name'] == data['name']
        assert response.data['level'] == data['level']

    def test_it_returns_error_if_provider_name_exists(self, api_client):
        provider = ProviderFactory(name='First Factory', level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        data = {
            'name': provider.name,
            'level': Provider.ProviderLevelChoices.FIRST_LEVEL,
        }

        response = api_client.post('/api/providers/', data=data, format='json')

        assert response.status_code == 400
        assert response.data['name'][0] == 'Provider already exists.'

    def test_it_creates_second_level_in_retail_chain(self, api_client):
        provider = ProviderFactory(name='First level', provider=None, level=0)
        customer = CustomerFactory.build()
        data = {
            'name': customer.name,
            'provider': provider.pk,
            'level': Provider.ProviderLevelChoices.SECOND_LEVEL,
        }

        response = api_client.post('/api/providers/', data=data, format='json')

        assert response.status_code == 201
        assert response.data['name'] == data['name']
        assert response.data['provider'] == data['provider']
        assert response.data['level'] == data['level']

    def test_it_creates_third_level_in_retail_chain(self, api_client):
        provider_1 = ProviderFactory(name='First level', provider=None, level=0)
        provider_2 = ProviderFactory(
            name='Second level', provider=provider_1, level=Provider.ProviderLevelChoices.SECOND_LEVEL
        )
        customer = CustomerFactory.build()
        data = {
            'name': customer.name,
            'provider': provider_2.pk,
            'level': Provider.ProviderLevelChoices.THIRD_LEVEL,
        }

        response = api_client.post('/api/providers/', data=data, format='json')

        assert response.status_code == 201
        assert response.data['name'] == data['name']
        assert response.data['provider'] == data['provider']
        assert response.data['level'] == data['level']

    def test_it_creates_fourth_level_in_retail_chain(self, api_client):
        provider_1 = ProviderFactory(name='First level', provider=None, level=0)
        provider_2 = ProviderFactory(
            name='Second level', provider=provider_1, level=Provider.ProviderLevelChoices.SECOND_LEVEL
        )
        provider_3 = ProviderFactory(
            name='Third level', provider=provider_2, level=Provider.ProviderLevelChoices.THIRD_LEVEL
        )
        customer = CustomerFactory.build()
        data = {
            'name': customer.name,
            'provider': provider_3.pk,
            'level': Provider.ProviderLevelChoices.FOURTH_LEVEL,
        }

        response = api_client.post('/api/providers/', data=data, format='json')

        assert response.status_code == 201
        assert response.data['name'] == data['name']
        assert response.data['provider'] == data['provider']
        assert response.data['level'] == data['level']

    def test_it_creates_fifth_level_in_retail_chain(self, api_client):
        provider_1 = ProviderFactory(name='First level', provider=None, level=0)
        provider_2 = ProviderFactory(
            name='Second level', provider=provider_1, level=Provider.ProviderLevelChoices.SECOND_LEVEL
        )
        provider_3 = ProviderFactory(
            name='Third level', provider=provider_2, level=Provider.ProviderLevelChoices.THIRD_LEVEL
        )
        provider_4 = ProviderFactory(
            name='Fourth level', provider=provider_3, level=Provider.ProviderLevelChoices.FOURTH_LEVEL
        )
        customer = CustomerFactory.build()
        data = {
            'name': customer.name,
            'provider': provider_4.pk,
            'level': Provider.ProviderLevelChoices.FIFTH_LEVEL,
        }

        response = api_client.post('/api/providers/', data=data, format='json')

        assert response.status_code == 201
        assert response.data['name'] == data['name']
        assert response.data['provider'] == data['provider']
        assert response.data['level'] == data['level']
