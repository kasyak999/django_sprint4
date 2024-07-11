from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
# get_list_or_404
from django.http import HttpResponse, HttpRequest
from blog.models import Post, Category, User, UserComments
from django.utils import timezone

from django.views.generic import (
    DetailView, UpdateView, ListView, CreateView, DeleteView
)
from django.urls import reverse_lazy

from django.core.paginator import Paginator
from django.db.models import Q
from .forms import MainForm, AddForm, AddPostForm
# from django import forms
from django.db.models import Count


class AddCommentCreateView(CreateView):
    """Добавление коментариев"""

    model = UserComments
    template_name = 'blog/comment.html'
    form_class = AddPostForm
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_object()
        return super().form_valid(form)

    def get_object(self):
        return Post.objects.get(pk=self.kwargs['post_id'])

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class ProfileDetailView(DetailView):
    """Просмотреть профиль пользователя"""

    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'  # Используйте username вместо pk
    slug_url_kwarg = 'username'  # Соответствующее имя в URL
    context_object_name = 'profile'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            user_posts = Post.objects.filter(
                Q(
                    is_published=True, category__is_published=True,
                    pub_date__lt=timezone.now(), author=self.object
                ) | Q(author=self.request.user)
            ).select_related('location', 'category', 'author')
        else:
            user_posts = Post.objects.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lt=timezone.now(),
                author_id=self.object.id
            ).select_related('location', 'category', 'author')

        paginator = Paginator(user_posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(UpdateView):
    """Изменение профиля пользователя"""

    model = User
    fields = (
        'username', 'first_name', 'last_name', 'email'
    )
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class IndexListView(ListView):
    """Главная страница"""

    queryset = Post.objects.main_filter()
    template_name = 'blog/index.html'
    paginate_by = 10
    context_object_name = 'post_list'

    def get_queryset(self):
        return (
            super().get_queryset().annotate(
                comment_count=Count("usercomments")
            )
        )


class CreateCreateView(CreateView):
    """Создание нового поста"""

    model = Post
    form_class = AddForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        """Только для авторизированых"""
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(
        Post.objects.main_filter(),
        id=pk,
    )
    return render(request, 'blog/detail.html', {'post': post})


class PostDetail(DetailView):
    """Пост подробнее"""

    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        result = UserComments.objects.filter(
            post_id=self.object.id
        ).select_related('author')
        form = AddPostForm()

        context = super().get_context_data(**kwargs)
        context['comments'] = result
        context['form'] = form
        return context

    def get_queryset(self):
        result = super().get_queryset().select_related('author')
        return result


class PostUpdateView(UpdateView):
    """Изменение поста пользователя"""

    model = Post
    form_class = AddForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect(
                'blog:post_detail', kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        result = super().get_queryset().filter(
            pk=self.kwargs['post_id'],
        )
        return result

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )


class PostUserDeleteView(DeleteView):
    """Удаление поста"""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MainForm(instance=self.object)
        return context

    def get_queryset(self):
        result = super().get_queryset().filter(
            pk=self.kwargs['post_id'],
        )
        return result

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect(
                'blog:post_detail', kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)


class CategoryPostsListView(ListView):
    """Вывод постов в категории"""

    context_object_name = 'post_list'
    template_name = 'blog/category.html'
    paginate_by = 10
    category = None

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return self.category.posts.filter(
            is_published=True,
            pub_date__lt=timezone.now()
        ).select_related('location', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context['category'] = self.category
        return context
