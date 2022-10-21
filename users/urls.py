from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from . import views

urlpatterns = [
    path("accounts/", views.ListCreateAccountView.as_view(), name="account-register"),
    path("login/", ObtainAuthToken.as_view(), name="login"),
    path(
        "accounts/newest/<int:num>/",
        views.ListAccountByDateView.as_view(),
        name="list-view",
    ),
    path("accounts/<pk>/", views.UpdateAccountView.as_view(), name="account-update"),
    path(
        "accounts/<pk>/management/",
        views.DeactivateAccountView.as_view(),
        name="account-manager",
    ),
]
