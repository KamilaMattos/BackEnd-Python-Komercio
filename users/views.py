from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from users.permissions import CustomAdminPermission, IsAccountOwner

from .models import User

from .serializers import (
    AccountDeactivateSerializer,
    AccountSerializer,
    AccountUpdateSerializer,
)


class ListCreateAccountView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer


class ListAccountByDateView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        url_num = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:url_num]


class UpdateAccountView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAccountOwner]
    queryset = User.objects.all()
    serializer_class = AccountUpdateSerializer


class DeactivateAccountView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomAdminPermission]
    queryset = User.objects.all()
    serializer_class = AccountDeactivateSerializer
