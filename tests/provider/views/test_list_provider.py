import pytest
from provider.models.provider import Provider
from tests.provider.factories import ProviderFactory, CustomerFactory, ContactFactory, ProductFactory


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

    def test_get_providers_with_contacts_products(self, api_client):
        provider_1 = ProviderFactory(name='First level', provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        provider_2 = CustomerFactory(
            name='Second level', provider=provider_1, level=Provider.ProviderLevelChoices.SECOND_LEVEL
        )
        contact1 = ContactFactory(city='Minsk', provider=provider_1)
        contact2 = ContactFactory(city='Grodno', provider=provider_1)
        contact3 = ContactFactory(city='Brest', provider=provider_2)

        product1 = ProductFactory(name='Product', provider=provider_1)
        product2 = ProductFactory(name='Another Product', provider=provider_2)

        response = api_client.get('/api/providers/')

        assert response.status_code == 200
        assert response.data[0]['contacts'][0]['city'] == contact1.city
        assert response.data[0]['contacts'][1]['city'] == contact2.city
        assert response.data[1]['contacts'][0]['city'] == contact3.city
        assert response.data[0]['products'][0]['name'] == product1.name
        assert response.data[1]['products'][0]['name'] == product2.name
