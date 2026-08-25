from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.permissions import AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly
from .paginations import CustomArticlePagination
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author').all()
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CustomArticlePagination

    def perform_create(self, serializer):
        serializer.save(author= self.request.user)

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['is_approved']
    search_fields = ['title', 'content']
    ordering_fields = ['id','title']

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
        