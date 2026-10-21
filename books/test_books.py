import pytest 
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from books.models import Book, UserProfile
from django.urls import reverse
from .serializers import BookSerializer

User = get_user_model()

@pytest.mark.django_db
def test_book_str():
    user = User.objects.create_user(username="testuser", password="password123")
    book = Book.objects.create(
        title="Python Deep Work", 
        author= "Abdurohman Ali",
        price = 600.00, 
        owner = user
    )
    assert str(book) == "Python Deep Work - Abdurohman Ali"
@pytest.mark.django_db
def test_user_profile_signal():
    user = User.objects.create_user(username="profileuser", password="password123")

    assert user.profile is not None
    assert str(user.profile) == "profileuser"

@pytest.mark.django_db
def test_book_serializer_invalid_price():
    invalid_data = {
        "title": "Python Deep Work",
        "author": "Abdurohman Ali",
        "description": "Django and DRF testing with Pytest tutorial.",
        "category": "Technology",
        "price": 34.00
    }
    serializer = BookSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert "price" in serializer.errors
@pytest.mark.django_db
def test_book_serializer_biography_price():
   invalid_data = {
           "title": "Python Deep Work",
           "author": "Abdurohman Ali",
           "description": "Django and DRF testing with Pytest tutorial.",
           "category": "Biography",
           "price": 200.00
       }
   serializer = BookSerializer(data=invalid_data)
   assert not serializer.is_valid()
   assert "price" in serializer.errors

@pytest.mark.django_db
def test_get_book_list():
    client = APIClient()
    url = reverse('book-list-create')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) > 0
@pytest.mark.django_db
def test_create_book_authenticated():
    user = User.objects.create_user(username="abdurohman", password="abdu1234")
    payload = {
        "title": "Python Deep Work",
        "author": "Abdurohman Ali",
        "description": "Django and DRF testing with Pytest tutorial.",
        "category": "Biography",
        "price": 700.00,
    }
    client = APIClient()
    client.force_authenticate(user = user)
    url = reverse('book-list-create')
    response = client.post(url,payload, format="json")

    assert response.status_code == 201
    assert response.data['title'] == "Python Deep Work"

@pytest.mark.django_db
def test_create_book_unauthenticated():
    payload = {
        "title": "Python Deep Work",
        "author": "Abdurohman Ali",
        "description": "Django and DRF testing with Pytest tutorial.",
        "category": "Biography",
        "price": 700.00,
    }    
    client = APIClient()
    url = reverse('book-list-create')
    response = client.post(url,payload, format="json")

    assert response.status_code == 401

@pytest.mark.django_db
def test_update_book_owner():
    user = User.objects.create_user(username="abdurohman", password="abdu1234")
    book = Book.objects.create(
        title="Python Deep Work",
        description = "Django and DRF testing with Pytest tutorial.",
        author= "Abdurohman Ali",
        category= "Technology",
        price = 600.00, 
        owner = user
    )
    payload = {
        "title": "Update Python Deep Work",
        "author": "Abdurohman Ali",
        "description": "Django and DRF testing with Pytest tutorial.",
        "category": "Biography",
        "price": 700.00,
    }
    client = APIClient()
    client.force_authenticate(user = user)
    url = reverse('book-detail', args=[book.id])
    response = client.put(url, payload , format="json")

    assert response.status_code == 200
    assert response.data['title'] == "Update Python Deep Work"
