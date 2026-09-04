from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Article
from .serializers import ArticleSerializer, ChangePasswordSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import ISOwnerAdminForDeleteOnly
from .paginations import CustomArticlePagination
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author').all()
    serializer_class = ArticleSerializer
    permission_classes = [ISOwnerAdminForDeleteOnly]
    pagination_class = CustomArticlePagination

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author= self.request.user)
        else:
            serializer.save()

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
    
class UserProfileview(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request':request })
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'የይለፍ ቃልህ ብስኬት ተቀይሯል!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
