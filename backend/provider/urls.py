from provider.views.provider_views import ProviderListCreateAPIView
from django.urls import path

urlpatterns = [
    path(
        '',
        ProviderListCreateAPIView.as_view(),
        name='list-create-provider',
    ),
]
