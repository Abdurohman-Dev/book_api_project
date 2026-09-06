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
            password=validated_data['password']
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
    def validate_price(self, value):
        if value < 0 :
            raise serializers.ValidationError("የመጽሃፉ ዋጋ ከ 0 ማነስ የለበትም!")
        return value
    def validate(self, data):
        title = data.get('title')
        author = data.get('author')
        category = data.get('category')
        price = data.get('price')
        if title and author and title.lower() == author.lower():
            raise serializers.ValidationError({"title":"የመጽሃፉ ርዕስና የደራሲው ስም አንድ አይነት መሆን የለባቸውም!"})
        if category == 'Biography' and price is not None and  price < 500:
            raise serializers.ValidationError({"price":"የ Biography መጽሃፍ ዋጋ ክ 500 ማነስ የለበትም!"})
        return data
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name']
        read_only_fields = ['id','username']
class ProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required= False)
    class Meta:
        model = UserProfile
        fields = ['id','bio','image']
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required= True, write_only= True)
    new_password = serializers.CharField(required= True, write_only= True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("የቀደመው የይለፍ ቃልህ ትክክል አይደለም።")
        return value
            