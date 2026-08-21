from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title