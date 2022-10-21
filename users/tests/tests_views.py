from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.views import status

from users.serializers import AccountSerializer
from users.models import User


class TestAccountRegisterView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = reverse("account-register")
        cls.login_url = reverse("login")

        cls.user_data = {
            "username": "logan",
            "password": "1234",
            "first_name": "logan",
            "last_name": "mattos",
            "is_seller": True,
        }

        cls.user_data2 = {
            "username": "yoshi",
            "password": "1234",
            "first_name": "yoshi",
            "last_name": "mattos",
            "is_seller": False,
        }

        cls.user_data3 = {
            "username": "sandy",
            "password": "1234",
            "first_name": "sandy",
            "last_name": "mattos",
            "is_seller": True,
        }

        cls.user_data4 = {
            "username": "sandy",
            "password": "1234",
            "first_name": "sandy",
            "last_name": "mattos",
            "is_seller": False,
        }

        cls.expect_return_fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        )

    def test_register_seller_account(self):
        response = self.client.post(self.base_url, self.user_data)
        returned_fields = tuple(response.data.keys())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["is_seller"], True)
        self.assertTupleEqual(returned_fields, self.expect_return_fields)

    def test_register_no_seller_account(self):
        response = self.client.post(self.base_url, self.user_data2)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["is_seller"], False)

    def test_no_possible_create_account_with_wrog_keys(self):
        seller_response = self.client.post(self.base_url, self.user_data3)
        seller_serializer = AccountSerializer(data=self.user_data3)

        self.assertEqual(seller_response.status_code, 400)
        self.assertEqual(seller_response.data, seller_serializer.errors)

    def test_no_possible_create_no_seller_account_with_wrog_keys(self):
        no_seller_response = self.client.post(self.base_url, self.user_data4)
        seller_serializer = AccountSerializer(data=self.user_data4)
        seller_serializer.is_valid()

        self.assertEqual(no_seller_response.status_code, 400)
        self.assertEqual(no_seller_response.data, seller_serializer.errors)

    def test_with_login_returns_seller_token(self):
        User.objects.create_user(**self.user_data)

        response = self.client.post(self.login_url, self.user_data)

        self.assertEqual(200, response.status_code)
        self.assertIn("token", response.data)

    def test_with_login_returns_no_seller_token(self):
        User.objects.create_user(**self.user_data2)

        response = self.client.post(self.login_url, self.user_data2)

        self.assertEqual(200, response.status_code)
        self.assertIn("token", response.data)

    def test_anyone_can_list_users(self):
        self.client.post(self.base_url, self.user_data)
        self.client.post(self.base_url, self.user_data2)

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)


class TestUpdateAccountView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "username": "logan",
            "password": "1234",
            "first_name": "logan",
            "last_name": "mattos",
            "is_seller": True,
        }

        cls.user_data2 = {
            "username": "yoshi",
            "password": "1234",
            "first_name": "yoshi",
            "last_name": "mattos",
            "is_seller": False,
        }

        cls.admin_user_data = {
            "username": "kamila",
            "password": "1234",
            "first_name": "kamila",
            "last_name": "muller",
            "is_seller": False,
        }

        owner_account = User.objects.create_user(**cls.user_data)
        regular_account = User.objects.create_user(**cls.user_data2)
        admin_account = User.objects.create_superuser(**cls.admin_user_data)

        cls.owner_token = Token.objects.create(user=owner_account)
        cls.regular_token = Token.objects.create(user=regular_account)
        cls.admin_token = Token.objects.create(user=admin_account)

        cls.update_url = reverse("account-update", kwargs={"pk": owner_account.id})
        cls.manager_url = reverse("account-manager", kwargs={"pk": owner_account.id})

        cls.data_to_update = {
            "first_name": "first name updated",
            "last_name": "last name updated",
        }
        cls.data_to_deactivate = {"is_active": False}

    def test_owner_can_edit_own_account(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.owner_token.key)
        response = self.client.patch(self.update_url, self.data_to_update)

        expected_status = status.HTTP_200_OK
        response_status = response.status_code

        self.assertEqual(expected_status, response_status)
        self.assertEqual(self.data_to_update["first_name"], response.data["first_name"])
        self.assertEqual(self.data_to_update["last_name"], response.data["last_name"])

    def test_account_can_not_be_edited_by_no_owner_account(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.regular_token.key)
        response = self.client.patch(self.update_url, self.data_to_update)

        expected_status = status.HTTP_403_FORBIDDEN
        response_status = response.status_code

        self.assertEqual(expected_status, response_status)

    def test_admin_can_deactivate_account(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        response = self.client.patch(self.update_url, self.data_to_deactivate)

        expected_status = status.HTTP_200_OK
        response_status = response.status_code

        self.assertEqual(expected_status, response_status)
        self.assertEqual(
            response.data["is_active"], self.data_to_deactivate["is_active"]
        )

    def test_admin_can_activate_account(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        self.client.patch(self.manager_url, self.data_to_deactivate)

        response = self.client.patch(self.manager_url, {"is_active": True})

        expected_status = status.HTTP_200_OK
        response_status = response.status_code

        self.assertEqual(expected_status, response_status)
        self.assertEqual(response.data["is_active"], True)

    def test_no_admin_can_not_deactivate_account(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.regular_token.key)
        response = self.client.patch(self.manager_url, self.data_to_deactivate)

        expected_status = status.HTTP_403_FORBIDDEN
        response_status = response.status_code

        self.assertEqual(expected_status, response_status)

    def test_no_admin_can_not_activate_account(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        self.client.patch(self.manager_url, self.data_to_deactivate)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.regular_token.key)
        response = self.client.patch(self.manager_url, {"is_active": True})

        expected_status = status.HTTP_403_FORBIDDEN
        response_status = response.status_code

        self.assertEqual(expected_status, response_status)
