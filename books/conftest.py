import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.cache import cache
User = get_user_model()

@pytest.fixture(autouse=True)
def disable_throttling_and_clear_cache(settings):
    cache.clear()
    settings.REST_FRAMEWORK = {
        ** settings.REST_FRAMEWORK,
        'DEFAULT_THROTTLE_CLASSES': [],
        'DEFAULT_THROTTLE_RATES':{},
    }
@pytest.fixture
def api_client():
    return APIClient()
@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        defaults = {
            'username': 'testuser',
            'password': 'password123'
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    return make_user
@pytest.fixture
def authenticated_client(api_client,create_user):
    user = create_user()
    api_client.force_authenticate(user = user)
    return api_client, user
@pytest.fixture
def valid_book_data():
    return {
        "title": "Python Deep Work",
        "author": "Abdurohman Ali",
        "description": "Django and DRF testing with Pytest tutorial.",
        "category": "Technology",
        "price": 399.00
    }