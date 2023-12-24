import pytest

from tests.provider.factories import ProductFactory


class TestGet:
    @pytest.mark.django_db
    def test_get_product(self, api_client):
        product = ProductFactory(name='Product')

        response = api_client.get(f'/api/providers/product/{product.pk}/')

        assert response.status_code == 200


class TestPatch:
    @pytest.mark.django_db
    def test_it_updates_product(self, api_client):
        product = ProductFactory(name='Product')
        data = {'name': 'test product'}

        response = api_client.patch(f'/api/providers/product/{product.pk}/', data=data, format='json')

        product.refresh_from_db()
        assert response.status_code == 200
        assert response.data['name'] == product.name


class TestDelete:
    @pytest.mark.django_db
    def test_it_deletes_product(self, api_client):
        product = ProductFactory(name='Product')

        response = api_client.delete(f'/api/providers/product/{product.pk}/')

        assert response.status_code == 204
