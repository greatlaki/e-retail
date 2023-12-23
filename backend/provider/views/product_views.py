from drf_spectacular.utils import extend_schema
from rest_framework import generics
from provider.models.product import Product
from provider.serializers.product_serializers import ProductListCreateSerializer


@extend_schema(tags=['Product'])
class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductListCreateSerializer
    queryset = Product.objects.all()
