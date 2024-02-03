import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from faker import Faker
from django.contrib.auth import get_user_model
from accounts.models import UserDetail
import random
from rest_framework_simplejwt.tokens import RefreshToken

user = get_user_model()
fake = Faker()

data = {"email": fake.email(), "password": "1234!@#$"}


@pytest.fixture
def create_user():
    user_create = user.objects.create_user(**data)
    return user_create


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def credentials(api_client, create_user):
    user = create_user
    refresh = RefreshToken.for_user(user=user)
    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )
    return user, api_client


@pytest.mark.django_db
class TestAccountApi:

    def test_register_account_get(self, api_client, create_user, credentials):
        url = reverse("accounts:AccountApi:registration")
        response = api_client.get(url)
        user_get = user.objects.get(email=data["email"])
        assert response.status_code == 405
        assert user.objects.count() == 1
        assert UserDetail.objects.count() == 1
        assert user_get.is_active
        url_user_detail = reverse("accounts:AccountApi:profile")
        data_profile = {
            "FirstName": fake.first_name(),
            "LastName": fake.last_name(),
            "Gender": random.choice(["True", "False"]),
            "NationalCode": random.randint(1000000000, 9000000000),
            "Mobile": random.randint(9133100000, 9133109999),
        }
        response = api_client.patch(url_user_detail, data_profile)
        assert response.status_code == 200
        assert response.data["FirstName"] == data_profile["FirstName"]

    def test_user_doesnt_see_profile(self, api_client):
        user_object1 = user.objects.create_user(
            email=fake.email(), password="1234!@#$%"
        )
        data = {
            "FirstName": "mahdieh",
            "LastName": "mohammadi",
            "Gender": "true",
            "NationalCode": "4420290439",
            "Mobile": "09133747009",
        }
        url = reverse("accounts:AccountApi:profile")
        response = api_client.put(url, data)
        assert response.status_code == 401
        assert UserDetail.objects.count() == user.objects.count()

    def test_not_change_password_user(
        self, create_user, api_client, credentials
    ):
        url = reverse("accounts:AccountApi:ChangePass")
        data = {
            "oldpassword": "444",
            "newpassword": "12548!@#$%",
            "confirmpassword": "12548!@#$%",
        }
        response = api_client.put(url, data)
        assert response.status_code == 400

    def test_change_password_user(self, create_user, api_client, credentials):
        url = reverse("accounts:AccountApi:ChangePass")
        change_password = {
            "OldPassword": data["password"],
            "NewPassword": "12548!@#$%",
            "ConfirmPassword": "12548!@#$%",
        }
        response = api_client.put(url, change_password)
        assert response.status_code == 200

    def test_delete_users(self):
        for _ in range(20):
            user.objects.create_user(email=fake.email(), password="123456")
        user.objects.all().delete()
        assert user.objects.count() == 0
