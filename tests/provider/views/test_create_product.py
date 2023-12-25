import pytest
from tests.provider.factories import ProductFactory


@pytest.mark.django_db
class TestPost:
    def test_it_creates_product(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        product = ProductFactory.build()
        data = {'name': product.name, 'model': product.model}

        response = api_client.post('/api/providers/product/', data=data, format='json')

        assert response.status_code == 201

    def test_inactive_user_cannot_create_product(self, api_client, active_user):
        product = ProductFactory.build()
        data = {'name': product.name, 'model': product.model}

        response = api_client.post('/api/providers/product/', data=data, format='json')

        assert response.status_code == 401
        assert response.data['detail'] == 'Authentication credentials were not provided.'
