from provider.views.provider_views import ProviderListCreateAPIView
from provider.views.product_views import ProductListCreateAPIView
from django.urls import path

urlpatterns = [
    path('', ProviderListCreateAPIView.as_view(), name='list-create-providers'),
    path('products/', ProductListCreateAPIView.as_view(), name='list-create-products'),
]
