import pytest 
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from books.models import Book, UserProfile
from django.urls import reverse
from .serializers import BookSerializer, RegisterSerializer

User = get_user_model()
@pytest.mark.django_db
def test_non_owner_or_non_staff_user(api_client, create_user):
    user = create_user(username="book-owner")
    other_user = create_user(username="other-user")
    book = Book.objects.create(
        title="Python Deep Work", 
        author= "Abdurohman Ali",
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
    api_client.force_authenticate(user = other_user)
    url = reverse('book-detail', args=[book.id])
    response = api_client.put(url, payload, format='json')
    assert response.status_code == 403
@pytest.mark.django_db
def test_staff_user_can_update_book(api_client, create_user):
    owner = create_user(username="book-owner")
    staff_user = create_user(username="staff-user", is_staff = True)
    book = Book.objects.create(
        title="Python Deep Work", 
        author= "Abdurohman Ali",
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
    api_client.force_authenticate(user = staff_user)
    url = reverse('book-detail', args=[book.id])
    response = api_client.put(url, payload, format='json')
    assert response.status_code == 200
    assert response.data['title'] == "Update Python Deep Work"
@pytest.mark.django_db
def test_admin_user_can_update_book(api_client, create_user):
    owner = create_user(username="book-owner")
    admin_user = create_user(username="admin-user", is_superuser = True)
    book = Book.objects.create(
        title="Python Deep Work", 
        author= "Abdurohman Ali",
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
    api_client.force_authenticate(user = admin_user)
    url = reverse('book-detail', args=[book.id])
    response = api_client.put(url, payload, format='json')
    assert response.status_code == 200
    assert response.data['title'] == "Update Python Deep Work"
    response = api_client.delete(url)
    assert response.status_code == 204
@pytest.mark.django_db
def test_book_str(create_user):
    user = create_user(username="book-owner")
    book = Book.objects.create(
        title="Python Deep Work", 
        author= "Abdurohman Ali",
        price = 600.00, 
        owner = user
    )
    assert str(book) == "Python Deep Work - Abdurohman Ali"
@pytest.mark.django_db
def test_user_profile_signal(create_user):
    user =create_user(username="profileuser")
    assert user.profile is not None
    assert str(user.profile) == "profileuser"
def test_book_serializer_invalid_price(valid_book_data):
    data = valid_book_data.copy()
    data["price"] = 34.00

    serializer = BookSerializer(data=data)
    assert not serializer.is_valid()
    assert "price" in serializer.errors
def test_book_serializer_biography_price(valid_book_data):
    data = valid_book_data.copy()
    data["category"] = "Biography"
    data["price"] = 200.00
    serializer = BookSerializer(data=data)
    assert not serializer.is_valid()
    assert "price" in serializer.errors
@pytest.mark.django_db
def test_register_serialzer_password_mismatch():
    payload = {
        "username": "abdurohman",
        "email": "abdu@gmail.com",
        "password": "password123",
        "password2": "abdu1234"
    }
    serializer = RegisterSerializer(data= payload)
    assert not serializer.is_valid()
    assert "password" in serializer.errors

@pytest.mark.django_db
def test_get_book_list(api_client):
    url = reverse('book-list-create')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) > 0
@pytest.mark.django_db
def test_create_book_authenticated(authenticated_client):
    client, user = authenticated_client
    payload = {
        "title": "Python Deep Work",
        "author": "Abdurohman Ali",
        "description": "Django and DRF testing with Pytest tutorial.",
        "category": "Biography",
        "price": 700.00,
    }
    url = reverse('book-list-create')
    response = client.post(url,payload, format="json")

    assert response.status_code == 201
    assert response.data['title'] == "Python Deep Work"
@pytest.mark.django_db
def test_create_book_unauthenticated(api_client):
    payload = {
        "title": "Python Deep Work",
        "author": "Abdurohman Ali",
        "description": "Django and DRF testing with Pytest tutorial.",
        "category": "Biography",
        "price": 700.00,
    }    
    url = reverse('book-list-create')
    response = api_client.post(url,payload, format="json")

    assert response.status_code == 401
@pytest.mark.django_db
def test_update_book_owner(authenticated_client):
    client, user = authenticated_client
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
    url = reverse('book-detail', args=[book.id])
    response = client.put(url, payload , format="json")

    assert response.status_code == 200
    assert response.data['title'] == "Update Python Deep Work"

@pytest.mark.django_db
def test_permission_is_owner_or_read_only_for_anonymous_user(api_client, create_user):
    user = create_user(username="book_owner")
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
        "price": 700.00,
    }
    url = reverse('book-list-create')
    response = api_client.get(url)

    assert response.status_code == 200
    url = reverse('book-detail', args=[book.id])
    response = api_client.put(url, payload, format="json")
    assert response.status_code == 401
@pytest.mark.django_db
def test_permission_is_owner_or_read_only_for_non_owner(api_client, create_user):
    owner = create_user(username="book-owner")
    other_user = create_user(username="other-user")
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
    api_client.force_authenticate(user = other_user)
    url = reverse('book-detail', args=[book.id])
    response = api_client.put(url,payload, format="json")
    assert response.status_code == 403
@pytest.mark.django_db
def test_permission_delete_book_by_owner(api_client, create_user):
    owner = create_user(username="owner_user")
    other_user = create_user(username="other_user")
    book = Book.objects.create(
        title="Python Deep Work",
        description = "Django and DRF testing with Pytest tutorial.",
        author= "Abdurohman Ali",
        category= "Technology",
        price = 600.00, 
        owner = owner
    )
    api_client.force_authenticate(user = other_user)
    url = reverse('book-detail', args=[book.id])
    response = api_client.delete(url)
    assert response.status_code == 403
    api_client.force_authenticate(user = owner)
    response = api_client.delete(url)
    assert response.status_code == 204
@pytest.mark.django_db
def test_search_books_by_title(api_client, create_user):
    user = create_user(username="book-owner")
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
    url = reverse('book-list-create',) + '?search=Python'
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 1 
@pytest.mark.django_db
def test_books_pagination(api_client, create_user):
    user = create_user(username="book-owner")
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
    url = reverse('book-list-create') + '?page_size=10'
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['count'] == 15
    assert len(response.data['results']) == 10
    assert response.data['next'] is not None
@pytest.mark.django_db
def test_books_ordering(api_client, create_user):
    user = create_user(username="book-owner")
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
    url = reverse('book-list-create') + '?ordering=-price'
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['price'] == "600.00"
    assert response.data['results'][1]['price'] == "100.00"
