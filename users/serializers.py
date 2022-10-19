from rest_framework import serializers
from .models import User


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        ]
        extra_kwargs = {"is_seller": {"required": True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user

