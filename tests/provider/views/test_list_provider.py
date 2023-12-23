import pytest
from provider.models.provider import Provider
from tests.provider.factories import ProviderFactory, CustomerFactory


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
