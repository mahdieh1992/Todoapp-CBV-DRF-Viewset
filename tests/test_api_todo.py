import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from Todo.models import Todo


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def created_user():
    usermodel = get_user_model()
    user = usermodel.objects.create_user(
        email="test@gmail.com", password="12345"
    )
    return user



@pytest.fixture
def force_login(api_client, created_user):
    user = created_user
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def created_todo(force_login):
    api_client, user = force_login
    return Todo.objects.create(user=user, Title="this is test")


@pytest.mark.django_db
class TestApiTodo:

    def test_api_todo_get(self, api_client, created_todo):
        url = reverse("Todo:TodoApi:Todo-list")
        response = api_client.get(url)
        assert response.status_code == 200
        assert Todo is not None
        assert Todo.objects.count() == 1

    def test_api_todo_not_put(self, api_client, created_todo):
        data = {
            "Title": "this is changed",
            "Is_active": True,
            "Completed": True,
        }
        response = api_client.put(f"/Todo/api/v1/TodoDetail/{Todo.pk}", data)
        assert response.status_code == 404

    def test_api_todo_put(self, api_client, created_todo):

        data = {
            "Title": "this is changed",
            "Is_active": True,
            "Completed": True,
        }
        url = reverse(
            "Todo:TodoApi:TodoDetail", kwargs={"pk": created_todo.pk}
        )
        response = api_client.put(url, data)
        assert response.status_code == 200

    def test_api_todo_delete(self, api_client, created_todo):
        url = reverse(
            "Todo:TodoApi:TodoDetail", kwargs={"pk": created_todo.pk}
        )
        response = api_client.delete(url)
        assert response.status_code == 204
