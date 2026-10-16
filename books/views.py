from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from .models import Book , UserProfile
from .serializers import ( 
    RegisterSerializer,
    BookSerializer,
    ChangePasswordSerializer, 
    ProfileImageSerializer,
    UserProfileSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiParameter,OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .permissions import IsOwnerOrStaffCanEditDelete
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from rest_framework.views import APIView
from.pagination import BookPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.select_related('owner').all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['category','owner__username']
    search_fields = ['title','author','description']
    ordering_fields = ['price','published_date','created_at']

    @extend_schema(
            summary="የመጽሃፍ ዝርዝር ",
            description="መጽሃፍትን በ Catagory Titile ለመፈለግ ያገለግላል። ",
            tags=['Book Management'],
            parameters=[
                OpenApiParameter(
                    name= 'category',
                    type = OpenApiTypes.STR,
                    location= OpenApiParameter.QUERY,
                    description="የመጽሃፉን Category ይምረጡ",
                    enum=['Fiction','Non-Fiction','History','Biography','Science'],
                    default= 'Fiction'
                )
            ]
    )
    @extend_schema(
            summary="አድስ መጽሃፍ መመዝገቢያ",
            description="አድስ መጽሃፍ ለመመዝገብ ያገለግላል። ባለቤቱ በ (owner) በራስ-ሰር የሆናል።",
            tags=['Book Management'],
            examples=[
                OpenApiExample(
                    'Valid Book Example',
                    value={
                        'title': 'Python Deep Work',
                        'description': 'Mastering DRF step by step',
                        'category': 'Technology',
                        'author' : 'Abdurohman',
                        'price': 600
                    }
                )
            ]
    )
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.select_related('owner').all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrStaffCanEditDelete]

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
class ProfileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileImageSerializer

    @extend_schema(
            request={
                'multipart/form-data': {
                    'type': 'object',
                    'properties': {
                        'bio': {'type': 'string'},
                        'image': {'type': 'string', 'format': 'binary'},
                    },
                }
            },
            responses={200: ProfileImageSerializer}
    )
    def post(self, request, *args, **kwargs):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = ProfileImageSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ChangePasswordView(APIView): 
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user 
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "የይለፍ ቃልህ ብስኬት ተቀይሯል!"}, status=status.HTTP_200_OK)