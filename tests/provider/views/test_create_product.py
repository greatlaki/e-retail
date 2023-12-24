import pytest
from tests.provider.factories import ProductFactory


@pytest.mark.django_db
class TestPost:
    def test_it_creates_product(self, api_client):
        product = ProductFactory.build()
        data = {'name': product.name, 'model': product.model}

        response = api_client.post('/api/providers/product/', data=data, format='json')

        assert response.status_code == 201
