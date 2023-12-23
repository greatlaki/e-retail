import pytest
from tests.user.factories import UserFactory


@pytest.mark.django_db
class TestPost:
    def setup_method(self):
        self.email = 'test@example.com'
        self.password = 'testpassw0rd!'
        self.user = UserFactory(email=self.email)
        self.user.set_password(self.password)
        self.user.save()

        self.endpoint = '/api/users/login/'

    def test_user_login(self, api_client):
        data = {'email': self.email, 'password': self.password}

        response = api_client.post(self.endpoint, data=data)

        assert response.status_code == 200
        assert response.data['email'] == data['email']

    def test_it_returns_error_if_required_field_was_not_entered(self, client):
        data = {'email': self.email}

        response = client.post(self.endpoint, data=data)

        assert response.status_code == 400
        assert response.data['password'] == ['This field is required.']

    def test_it_returns_error_if_incorrect_username_was_entered(self, client):
        data = {'email': 'another@example.com', 'password': self.password}

        response = client.post(self.endpoint, data=data)

        assert response.status_code == 401
        assert response.data['detail'] == 'Invalid credentials, try it again'

    def test_it_returns_error_if_incorrect_password_was_entered(self, client):
        data = {'email': self.email, 'password': 'testpass'}

        response = client.post(self.endpoint, data=data)

        assert response.status_code == 401
        assert response.data['detail'] == 'Invalid credentials, try it again'
