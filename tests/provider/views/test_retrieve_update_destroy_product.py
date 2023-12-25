import pytest

from tests.provider.factories import ProductFactory


@pytest.mark.django_db
class TestGet:
    def test_get_product(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        product = ProductFactory(name='Product')

        response = api_client.get(f'/api/providers/product/{product.pk}/')

        assert response.status_code == 200

    def test_inactive_user_cannot_get_product(self, api_client):
        product = ProductFactory(name='Product')

        response = api_client.get(f'/api/providers/product/{product.pk}/')

        assert response.status_code == 401


@pytest.mark.django_db
class TestPatch:
    def test_it_updates_product(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        product = ProductFactory(name='Product')
        data = {'name': 'test product'}

        response = api_client.patch(f'/api/providers/product/{product.pk}/', data=data, format='json')

        product.refresh_from_db()
        assert response.status_code == 200
        assert response.data['name'] == product.name

    def test_inactive_user_cannot_update_product(self, api_client):
        product = ProductFactory(name='Product')
        data = {'name': 'test product'}

        response = api_client.patch(f'/api/providers/product/{product.pk}/', data=data, format='json')

        assert response.status_code == 401


@pytest.mark.django_db
class TestDelete:
    def test_it_deletes_product(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        product = ProductFactory(name='Product')

        response = api_client.delete(f'/api/providers/product/{product.pk}/')

        assert response.status_code == 204

    def test_inactive_user_cannot_delete_product(self, api_client):
        product = ProductFactory(name='Product')

        response = api_client.delete(f'/api/providers/product/{product.pk}/')

        assert response.status_code == 401
