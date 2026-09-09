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
def validate_no_number(value):
    if any(char.isdigit() for char in value):
        raise serializers.ValidationError("በደራሲው ስም ውስጥ ቁጥር ማስገባት አየቻልም!")
    return value

def validate_no_special_chars(value):
    if '#' in value or '@' in value:
        raise serializers.ValidationError("በዚህ ቦታ ላይ '@' and '#' መጠቀም አይቻልም! ")
    return value

class BookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    author = serializers.CharField(validators=[validate_no_number])
    title = serializers.CharField(validators=[validate_no_special_chars])

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description', 
            'category', 'price', 'published_date', 
            'owner', 'created_at'
        ]
    def validate_price(self, value):
        if value < 50: 
            raise serializers.ValidationError("የመጽሃፉ ዋጋ ከ 0 ማነስ የለበትም!")
        return value
    def validate(self, data):
        author = data.get('author')
        title = data.get('title')
        category = data.get('category')
        price = data.get('price')

        if author and title and author.lower() == title.lower() :
            raise serializers.ValidationError({"title": "የመጽሃፉ ርዕስ እና ደራሲው ስም ተመሳሳይ መሆን አይችሉም!"})
        if category == 'Biography' and price is not None and price < 500:
            raise serializers.ValidationError({"price": "የ Biography መጽሃፍ ዋጋ ከ 500 ብር ማነስ የለበትም! "})
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
