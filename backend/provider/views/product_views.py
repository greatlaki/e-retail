from drf_spectacular.utils import extend_schema
from rest_framework import generics
from provider.models.product import Product
from provider.serializers.product_serializers import ProductCreateSerializer, ProductRetrieveUpdateDestroySerializer


@extend_schema(tags=['Product'])
class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()


@extend_schema(tags=['Product'])
class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductRetrieveUpdateDestroySerializer
    queryset = Product.objects.all()

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return
