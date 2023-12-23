import pytest
from rest_framework.test import APIClient

from tests.user.factories import UserFactory


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture
def active_user():
    user = UserFactory()
    user.save()
    return user
