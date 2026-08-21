from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.permissions import AllowAny

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        article = self.get_object()
        article.is_approved = True
        article.save()
        return Response({'message': 'Article approved successfully!'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def approved_articles(self, request):
        approved = Article.objects.filter(is_approved=True)
        serializer = self.get_serializer(approved, many=True)
        return Response(serializer.data)