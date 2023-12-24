from provider.views.provider_views import (
    ProviderListCreateAPIView,
    ProviderRetrieveUpdateDestroyAPIView,
    ProviderStatisticAPIView,
)
from provider.views.product_views import ProductCreateAPIView, ProductRetrieveUpdateDestroyAPIView
from django.urls import path

urlpatterns = [
    # Provider
    path('', ProviderListCreateAPIView.as_view(), name='list-create-providers'),
    path('<int:pk>/', ProviderRetrieveUpdateDestroyAPIView.as_view(), name='retrieve-update-destroy-provider'),
    path('debt-statistic/', ProviderStatisticAPIView.as_view(), name='list-debt-statistic'),
    # Product
    path('product/', ProductCreateAPIView.as_view(), name='create-product'),
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='retrieve-update-destroy-product'),
]
