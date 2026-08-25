from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    reading_time = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'is_approved', 'author', 'reading_time']
        read_only_fields = ['author']

    def get_reading_time(self,obj):
        word_count = len(obj.content.split())
        minutes = round(word_count / 200, 2)
        return f"{minutes} min read " if minutes > 0 else "1 min read"