from django.shortcuts import render, get_object_or_404
# get_list_or_404
from django.http import HttpResponse, HttpRequest
from blog.models import Post, Category
from django.utils import timezone


MAX_ENTRIES = 5


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.main_filter()[:MAX_ENTRIES]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(
        Post.objects.main_filter(),
        id=pk,
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = category.posts.filter(
        is_published=True,
        pub_date__lt=timezone.now()
    ).select_related('location', 'author')
    return render(
        request, 'blog/category.html',
        {'category': category, 'post_list': posts}
    )
