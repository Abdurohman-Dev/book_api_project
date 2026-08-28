from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Article

User = get_user_model()

class ArticleAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='articleuser', 
            password='testpassword123'
        )
        
        self.article = Article.objects.create(
            title='Test Book',
            content='This is test content',
            author=self.user
        )

        # URLs
        self.articles_url = reverse('article-list')

    def test_get_article_list(self):
        response = self.client.get(self.articles_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
