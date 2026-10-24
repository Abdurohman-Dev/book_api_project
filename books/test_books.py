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

@pytest.mark.django_db
def test_permission_is_owner_or_read_only_for_anonymous_user():
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
    url = reverse('book-list-create')
    response = client.get(url)

    assert response.status_code == 200
    url = reverse('book-detail', args=[book.id])
    response = client.put(url, payload, format="json")
    assert response.status_code == 401
    
@pytest.mark.django_db
def test_permission_is_owner_or_read_only_for_non_owner():
    owner = User.objects.create_user(username="abdurohman", password="abdu1234")
    other_user = User.objects.create_user(username="testuser", password="password123")
    book = Book.objects.create(
        title="Python Deep Work",
        description = "Django and DRF testing with Pytest tutorial.",
        author= "Abdurohman Ali",
        category= "Technology",
        price = 600.00, 
        owner = owner
    )
    payload = {
        "title": "Update Python Deep Work",
        "author": "Abdurohman Ali",
        "description": "Django and DRF testing with Pytest tutorial.",
        "category": "Biography",
        "price": 700.00,
    }
    client = APIClient()
    client.force_authenticate(user = other_user)
    url = reverse('book-detail', args=[book.id])
    response = client.put(url,payload, format="json")
    assert response.status_code == 403

@pytest.mark.django_db
def test_permission_delete_book_by_owner():
    owner = User.objects.create_user(username="abdurohman", password="abdu1234")
    other_user = User.objects.create_user(username="testuser", password="password123")
    book = Book.objects.create(
        title="Python Deep Work",
        description = "Django and DRF testing with Pytest tutorial.",
        author= "Abdurohman Ali",
        category= "Technology",
        price = 600.00, 
        owner = owner
    )
    client = APIClient()
    client.force_authenticate(user = other_user)
    url = reverse('book-detail', args=[book.id])
    response = client.delete(url)

    assert response.status_code == 403
    client.force_authenticate(user = owner)
    response = client.delete(url)
    assert response.status_code == 204
@pytest.mark.django_db
def test_search_books_by_title():
    user = User.objects.create_user(username="abdurohman", password="abdu1234")
    book1 = Book.objects.create(
        title="Python Deep Work",
        description = "Django and DRF testing with Pytest tutorial.",
        author= "Abdurohman Ali",
        category= "Technology",
        price = 600.00, 
        owner = user
    )
    book2 = Book.objects.create(
        title="Django REST Framework",
        description = "Django and DRF testing with Pytest tutorial.",
        author= "Abdurohman Ali",
        category= "Technology",
        price = 600.00, 
        owner = user
    )
    client = APIClient()
    url = reverse('book-list-create',) + '?search=Python'
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 1 
@pytest.mark.django_db
def test_books_pagination():
    user = User.objects.create_user(username="abdurohman", password="abdu1234")
    books = [
        Book(
            title=f"Django REST Framework {i}",
            description = "Django and DRF testing with Pytest tutorial.",
            author= "Abdurohman Ali",
            category= "Technology",
            price = 600.00, 
            owner = user
        )
        for i in range(15)
    ]
    Book.objects.bulk_create(books)
    client = APIClient()
    url = reverse('book-list-create') + '?page_size=10'
    response = client.get(url)

    assert response.status_code == 200
    assert response.data['count'] == 15
    assert len(response.data['results']) == 10
    assert response.data['next'] is not None
@pytest.mark.django_db
def test_books_ordering():
    user = User.objects.create_user(username="abdurohman", password="abdu1234")
    book1 = Book.objects.create(
        title="Python Deep Work",
        description = "Django and DRF testing with Pytest tutorial.",
        author= "Abdurohman Ali",
        category= "Technology",
        price = 100.00, 
        owner = user
    )
    book2 = Book.objects.create(
        title="Django REST Framework",
        description = "Django and DRF testing with Pytest tutorial.",
        author= "Abdurohman Ali",
        category= "Technology",
        price = 600.00, 
        owner = user
    )
    client = APIClient()
    url = reverse('book-list-create') + '?ordering=-price'
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['price'] == "600.00"
    assert response.data['results'][1]['price'] == "100.00"
