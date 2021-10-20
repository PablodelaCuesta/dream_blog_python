from django.db import models
from django.contrib.auth import get_user_model
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

class Post(models.Model):
    title = models.CharField(max_length=120)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default= 0)
    view_count = models.IntegerField(default= 0)
    thumbnail = models.ImageField()
    featured = models.BooleanField()

    # content with tinymce
    content = HTMLField()

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
    def get_absoulute_url(self):
        return reverse('post-detail', kwargs={
            'id': self.id
        })