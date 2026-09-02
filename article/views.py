from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Article
from .serializers import ArticleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly
from .paginations import CustomArticlePagination
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import ChangePasswordSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author').all()
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CustomArticlePagination

    def perform_create(self, serializer):
        serializer.save(author= self.request.user)

    filter_backends = [DjangoFilterBackend, SearchFilter , OrderingFilter ]

    filterset_fields = ['is_approved', 'author']
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
class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response ({"message": "የይለፍ ቃልህ ብስኬት ተቀይሯል!"}, status = status.HTTP_200_OK)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserProfileview(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user