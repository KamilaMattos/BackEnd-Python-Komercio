from rest_framework import serializers
from .models import Product
from users.serializers import SellerSerializer


class ProductDetailedSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "description",
            "price",
            "quantity",
            "is_active",
        ]


class ProductGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "description",
            "price",
            "quantity",
            "is_active",
            "seller",
        ]


class ProductFilterSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller",
        ]

