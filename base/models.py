from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    pages = models.IntegerField()
    language = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='borrowed_books')

    def __str__(self):
        return self.title
    
