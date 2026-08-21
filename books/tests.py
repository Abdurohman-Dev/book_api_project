from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Test User መፍጠር
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@gmail.com', 
            password='testpassword123'
        )
        
        # Test Book መፍጠር
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            category='Fiction',
            price=200.00,
            published_date='2026-01-01',
            owner=self.user
        )

        # URLs
        self.login_url = reverse('token_obtain_pair')  # JWT Login URL
        self.book_list_url = reverse('book-list-create')  # Adjust based on your urls.py name

    def test_user_login(self):
        """የተጠቃሚ Login ፈተና"""
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_get_book_list(self):
        """የመጽሐፍት ዝርዝር ማየት (Public Read access)"""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_authenticated(self):
        """ተጠቃሚ Login አድርጎ መጽሐፍ መመዝገቡን መፈተሽ"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Book',
            'author': 'Author Name',
            'description': 'Description',
            'category': 'Fiction',
            'price': '150.00',
            'published_date': '2026-08-21'
        }
        response = self.client.post(self.book_list_url, data)
        print("\nDEBUG ERROR:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)