from django.db.models import query
from django.shortcuts import render
from .models import Post
from mail.models import Signup

def index(request):
    featured = Post.objects.filter(featured=True)
    latests = Post.objects.order_by('-timestamp')[0:3]

    if request.method == 'POST':
        
        # TODO: We need validation

        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'object_latest': latests
    }
    return render(request, 'index.html', context)

def blog(request):
    return render(request, 'blog.html', {})

def post(request):
    return render(request, 'post.html', {})