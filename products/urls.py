from django.urls import path
from . import views


urlpatterns = [
    path("products/", views.ListCreateProductView.as_view(), name="product-view"),
    path(
        "products/<pk>/",
        views.RetrieveUpdateProductView.as_view(),
        name="product-detail",
    ),
]
