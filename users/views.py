from django.contrib.auth import authenticate

from rest_framework import generics
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import AccountSerializer


class ListCreateAccountView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer


class ListAccountByDateView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        url_num = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:url_num]

