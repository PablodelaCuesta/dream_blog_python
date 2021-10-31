from django.db.models import query, Count, Q
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls.base import reverse

from posts.forms import PostForm
from .models import Post, Author
from mail.models import Signup

def get_author(user):
    qs = Author.objects.filter(user=user)

    if qs.exists():
        return qs[0]
    return None

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    context = {
        'queryset': queryset
    }

    return render(request, 'shared/search_result.html', context)

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

def contact(request):
    return render(request, 'contact.html', {})

def post(request, id):
    post = get_object_or_404(Post, id=id)
    most_recent = Post.objects.order_by('-timestamp')[:3]
    category_count = get_category_count()

    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count        
    }
    return render(request, 'post/post.html', context)

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)

    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'id': form.instance.id
            }))
    
    context = {
        'form': form
    }

    return render(request, "post_create.html", context)

def post_update(request):
    pass

def post_delete(request):
    pass