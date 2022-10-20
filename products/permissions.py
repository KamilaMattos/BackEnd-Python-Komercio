from rest_framework import permissions
from rest_framework.views import Request, View
from products.models import Product


class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_seller


class IsSellerProductOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Product) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.id == obj.seller.id
