from django.contrib import admin
from django.db import models
from .models import Author, Category, Post
from tinymce.widgets import TinyMCE

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)

# class contentAdmin(admin.ModelAdmin):
    
#     list_display = ["content"]
#     formfield_overrides = {
#         models.TextField: {'widget': TinyMCE()}
#     }

admin.site.register(Post)