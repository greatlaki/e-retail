import pytest

from tests.provider.factories import ProviderFactory, ContactFactory, ProductFactory

from provider.models.provider import Provider


class TestGet:
    @pytest.mark.django_db
    def test_get_provider(self, api_client):
        provider = ProviderFactory(name='First level', provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        ContactFactory(city='Minsk', provider=provider)
        ContactFactory(city='Grodno', provider=provider)
        ProductFactory(name='Product', provider=provider)

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


class TestDelete:
    @pytest.mark.django_db
    def test_it_deletes_provider(self, api_client):
        provider_1 = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)

        response = api_client.delete(f'/api/providers/{provider_1.pk}/')

        assert response.status_code == 204
