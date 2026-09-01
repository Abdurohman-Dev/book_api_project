from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, ChangePasswordView

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]