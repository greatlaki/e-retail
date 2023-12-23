from provider.views.provider_views import ProviderListCreateAPIView, ProviderRetrieveUpdateDestroyAPIView
from provider.views.product_views import ProductCreateAPIView, ProductRetrieveUpdateDestroyAPIView
from django.urls import path

urlpatterns = [
    # Provider
    path('', ProviderListCreateAPIView.as_view(), name='list-create-providers'),
    path('<int:pk>/', ProviderRetrieveUpdateDestroyAPIView.as_view(), name='retrieve-update-destroy-provider'),
    # Product
    path('product/', ProductCreateAPIView.as_view(), name='create-product'),
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='retrieve-update-destroy-product'),
]
