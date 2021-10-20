from django.db.models import query, Count
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from mail.models import Signup


def get_category_count():
    queryset = Post.objects\
        .values('categories__title')\
        .annotate(Count('categories__title'))
    return queryset

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
    page_request_var = 'page'

    category_count = get_category_count()
    post_list = Post.objects.all()
    most_recent = Post.objects.order_by('-timestamp')[:3]

    paginator = Paginator(post_list, 4)
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'most_recent': most_recent,
        'category_count': category_count
    }
    return render(request, 'blog.html', context)

def post(request, id):
    post = get_object_or_404(Post, id=id)
    context = {
        'post': post
    }
    return render(request, 'post.html', context)

