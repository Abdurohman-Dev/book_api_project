import pytest 
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from books.models import Book, UserProfile
from django.urls import reverse

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