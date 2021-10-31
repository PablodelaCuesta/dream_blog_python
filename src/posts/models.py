from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.base import Model
from django.urls import reverse
from tinymce.models import HTMLField


# Create your models here.

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self) -> str:
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.title

class Visit(models.Model):
    ip = models.CharField(max_length=120, primary_key=True)
    user_agent = models.CharField(max_length=255)

class PostView(models.Model):
    ip = models.CharField(max_length=120)
    user_agent = models.CharField(max_length=255)
    view_count = models.IntegerField(default= 0)  

class Post(models.Model):
    title = models.CharField(max_length=120)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default= 0)
    thumbnail = models.ImageField()
    featured = models.BooleanField()

    # content with tinymce
    content = HTMLField()

    views = models.ManyToManyField(PostView)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    previous_post = models.ForeignKey('self', related_name='previous' ,on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next',on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'id': self.id
        })
    
    def get_update_url(self):
        return reverse('post-update', kwargs={
            'id': self.id
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'id': self.id
        })

    

