from rest_framework import serializers
from .models import Article
from drf_spectacular.utils import extend_schema_field
from django.contrib.auth.models import User

class ArticleSerializer(serializers.ModelSerializer):
    reading_time = serializers.SerializerMethodField()
    author_full_name = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'is_approved', 'author', 'author_full_name', 'reading_time']
        read_only_fields = ['author']

    @extend_schema_field(serializers.CharField)
    def get_reading_time(self,obj):
        word_count = len(obj.content.split())
        minutes = round(word_count / 200, 2)
        return f"{minutes} min read " if minutes > 0 else "1 min read"

    @extend_schema_field(serializers.IntegerField)
    def get_author_full_name(self, obj):
        if obj.author:
            full_name = f"{obj.author.first_name} {obj.author.last_name}".strip()
            return full_name if full_name else obj.author.username
        return "Unknown"
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id','username']
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError("የቀደመው የይለፍ ቃልህ ትክክል አይደለም።")
        return value
