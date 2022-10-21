from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from . import views

urlpatterns = [
    path("accounts/", views.ListCreateAccountView.as_view()),
    path("login/", ObtainAuthToken.as_view()),
    path("accounts/newest/<int:num>/", views.ListAccountByDateView.as_view()),
    path("accounts/<pk>/", views.UpdateAccountView.as_view()),
    path("accounts/<pk>/management/", views.DeactivateAccountView.as_view()),
]
