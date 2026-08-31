from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name = validated_data['first_name']
        )
        return user

class BookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description', 
            'category', 'price', 'published_date', 
            'owner', 'created_at'
        ]
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name']
        read_only_fields = ['id','username']
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only= True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("የቀደመው የይለፍ ቃልህ ትክክል አይደለም።")
class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','bio','image']