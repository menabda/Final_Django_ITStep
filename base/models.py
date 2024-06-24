from django.db import models
from languages_plus.models import Language
from countries_plus.models import Country
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    origin = models.ForeignKey(Country,on_delete=models.SET_NULL, null=True, blank=True, related_name='authors')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.surname}'



class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL,null=True, blank=True, related_name='books')
    publisher = models.CharField(max_length=100)
    pages = models.IntegerField()
    language = models.ForeignKey(Language,on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)
    user = models.ManyToManyField(User, null=True, blank=True, related_name='borrowed_books')
    quantity = models.IntegerField(default=0)

   
    def belongs_to_user(self, user):
        return user in self.user.all()

    def __str__(self):
        return self.title
    
