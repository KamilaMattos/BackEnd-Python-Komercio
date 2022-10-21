from django.test import TestCase
from users.models import User
from products.models import Product


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.product_data = {
            "description": "Cadeira gamer",
            "price": 100.00,
            "quantity": 3,
            "is_active": True,
        }

        cls.user_data = {
            "username": "yoshi",
            "first_name": "Yoshi",
            "last_name": "Mattos",
            "is_seller": True,
        }

        cls.user_data2 = {
            "username": "logan",
            "first_name": "Logan",
            "last_name": "Mattos",
            "is_seller": True,
        }

        cls.user = User.objects.create_user(**cls.user_data)
        cls.product = Product.objects.create(**cls.product_data, seller=cls.user)
        cls.user2 = User.objects.create_user(**cls.user_data2)

    def test_account_fields(self):
        self.assertEqual(self.product_data["description"], self.product.description)
        self.assertEqual(self.product_data["price"], self.product.price)
        self.assertEqual(self.product_data["quantity"], self.product.quantity)
        self.assertEqual(self.product_data["is_active"], self.product.is_active)

    def test_account_fields_param(self):
        product_test = Product.objects.get(id=self.product.id)

        price_max_digits = product_test._meta.get_field("price").max_digits
        price_decimal_places = product_test._meta.get_field("price").decimal_places

        self.assertEqual(price_max_digits, 10)
        self.assertEqual(price_decimal_places, 2)

    def test_product_can_not_have_multiple_sellers(self):
        self.assertIn(
            self.product, self.user.products.filter(description="Cadeira gamer")
        )

        self.user2.products.add(self.product)

        self.assertNotIn(
            self.product, self.user.products.filter(description="Cadeira gamer")
        )
        self.assertIn(
            self.product, self.user2.products.filter(description="Cadeira gamer")
        )
