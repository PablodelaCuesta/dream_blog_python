from django.db.models import query
from django.shortcuts import render
from .models import Post

def index(request):
    featured = Post.objects.filter(featured=True)
    latests = Post.objects.order_by('-timestamp')[0:3]
    context = {
        'object_list': featured,
        'object_latest': latests
    }
    return render(request, 'index.html', context)

def blog(request):
    return render(request, 'blog.html', {})

def post(request):
    return render(request, 'post.html', {})