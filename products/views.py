from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from products.models import Product
from products.permissions import IsSellerOrReadOnly, IsSellerProductOwner
from products.serializers import (
    ProductFilterSerializer,
    ProductGeneralSerializer,
    ProductDetailedSerializer,
)

from utils.mixins import SerializerByMethodMixin


class ListCreateProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    permission_classes = [IsSellerOrReadOnly]
    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductGeneralSerializer,
        "POST": ProductDetailedSerializer,
    }
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class RetrieveUpdateProductView(
    SerializerByMethodMixin,
    generics.RetrieveUpdateAPIView,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerProductOwner]
    queryset = Product.objects.all()
    serializer_map = {
        "GET": ProductFilterSerializer,
        "PATCH": ProductDetailedSerializer,
    }
