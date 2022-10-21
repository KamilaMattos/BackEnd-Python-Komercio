from django.db.utils import IntegrityError
from django.test import TestCase
from users.models import User
from products.models import Product


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "username": "yoshi",
            "first_name": "Yoshi",
            "last_name": "Mattos",
            "is_seller": True,
        }

        cls.product_data = {
            "description": "Cadeira gamer",
            "price": 100.00,
            "quantity": 3,
            "is_active": True,
        }

        cls.user = User.objects.create_user(**cls.user_data)
        cls.products = [
            Product.objects.create(**cls.product_data, seller=cls.user)
            for _ in range(10)
        ]

    def test_account_fields(self):
        self.assertEqual(self.user_data["username"], self.user.username)
        self.assertEqual(self.user_data["first_name"], self.user.first_name)
        self.assertEqual(self.user_data["last_name"], self.user.last_name)
        self.assertEqual(self.user_data["is_seller"], self.user.is_seller)

    def test_account_fields_param(self):
        user_test = User.objects.get(username="yoshi")

        username = user_test._meta.get_field("username").max_length
        first_name = user_test._meta.get_field("first_name").max_length
        last_name = user_test._meta.get_field("last_name").max_length

        self.assertEqual(username, 20)
        self.assertEqual(first_name, 50)
        self.assertEqual(last_name, 50)

    def test_can_have_many_products(self):
        self.assertEqual(len(self.products), self.user.products.count())

        for product in self.products:
            self.assertEqual(self.user, product.seller)

    def test_user_have_unique_username(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(**self.user_data)
