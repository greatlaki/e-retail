import pytest
from provider.models.provider import Provider
from tests.provider.factories import ProviderFactory, ProductFactory


@pytest.mark.django_db
class TestPost:
    def test_it_creates_product(self, api_client):
        provider = ProviderFactory(provider=None, level=Provider.ProviderLevelChoices.FIRST_LEVEL)
        product = ProductFactory.build()
        data = {
            'name': product.name,
            'model': product.model,
            'provider': provider.pk,
        }

        response = api_client.post('/api/providers/product/', data=data, format='json')

        assert response.status_code == 201
