import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Book, UserProfile
from .serializers import BookSerializer

User = get_user_model()

@pytest.mark.django_db
def test_register_user_success(api_client):
    payload = {
        "username": "abdurohman",
        "email": "abdu@gmail.com",
        "password": "abdu1234",
        "password2": "abdu1234"
    }
    url = reverse('register')
    response = api_client.post(url,payload, format="json")

    assert response.status_code == 201
    User.objects.filter(username="abdurohman").exists()

@pytest.mark.django_db
def test_get_user_profile(api_client, create_user):
    user = create_user(username="abdurohman")
    api_client.force_authenticate(user=user)
    url = reverse('user-profile')
    response = api_client.get(url)

    assert response.status_code == 200

@pytest.mark.django_db
def test_change_password_success(authenticated_client):
    client, user = authenticated_client
    payload= {
        "old_password": "password123",
        "new_password": "abdu4321"
    }
    url = reverse('change-password')
    response = client.put(url, payload, format="json")

    assert response.status_code == 200
    assert user.check_password("abdu4321")