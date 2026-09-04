from django.db import models
from django.contrib.auth.models import User 
class Article(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title