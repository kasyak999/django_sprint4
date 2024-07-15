
from django.shortcuts import get_object_or_404, redirect
from blog.models import Post, Category, User, Comments
from django.utils import timezone

from django.views.generic import (
    DetailView, UpdateView, ListView, CreateView, DeleteView
)
from django.urls import reverse_lazy

from django.core.paginator import Paginator
from .forms import MainForm, AddForm, AddPostForm
# from django import forms
from django.db.models import Count
from django.contrib.auth.mixins import UserPassesTestMixin


# ####################Миксины#####################################
class PostSuccessUrl():
    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )


class UserSuccessUrl():
    """Перенаправление на страницк пользователя"""

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class OnlyAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect(
                'blog:post_detail', kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)


class UserPassesMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return True
        return False
# #####################################################


class IndexListView(ListView):
    """Главная страница"""

    model = Post
    # queryset = Post.main_filter.all()
    # Неработает почему то, объясни что не так с ним
    template_name = 'blog/index.html'
    paginate_by = 10
    # context_object_name = 'page_obj'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author', 'category', 'location'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=timezone.now()
        ).annotate(comment_count=Count('comment')).order_by('-pub_date')


class CategoryPostsListView(ListView):  # DetailView
    """Вывод постов в категории"""

    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True
        )
        return category.posts.filter(
            category__slug=category_slug,
            is_published=True,
            pub_date__lt=timezone.now()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['category'] = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True
        )
        return context


class PostDetail(DetailView):
    """Пост подробнее"""

    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        result = Comments.objects.filter(
            post_id=self.object.id
        ).select_related('author')
        form = AddPostForm()

        context = super().get_context_data(**kwargs)
        context['comments'] = result
        context['form'] = form
        return context

    def get_object(self):
        result = super().get_object()
        if result.author != self.request.user:
            return get_object_or_404(
                self.get_queryset(), is_published=True,
                category__is_published=True,
                pub_date__lt=timezone.now(),
                pk=self.kwargs['pk']
            )
        return result


class CreateCreateView(UserPassesMixin, UserSuccessUrl, CreateView):
    """Создание нового поста"""

    model = Post
    form_class = AddForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUserDeleteView(UserPassesMixin, OnlyAuthorMixin, DeleteView):
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
        ).order_by('created_at',)
        return result


class PostUpdateView(
    UserPassesMixin, OnlyAuthorMixin, PostSuccessUrl, UpdateView
):
    """Измененить пост пользователя"""

    model = Post
    form_class = AddForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        result = super().get_queryset().filter(
            pk=self.kwargs['post_id'],
        ).order_by('created_at',)
        return result


class ProfileDetailView(DetailView):
    """Просмотреть профиль пользователя"""

    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'  # Используйте username вместо pk
    slug_url_kwarg = 'username'  # Соответствующее имя в URL
    context_object_name = 'profile'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        if self.object == self.request.user:
            user_posts = Post.objects.filter(author=self.object)
        else:
            user_posts = Post.objects.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lt=timezone.now(), author=self.object
            )
        user_posts = user_posts.annotate(
            comment_count=Count("comment")
        ).order_by('-pub_date')

        paginator = Paginator(user_posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(UserPassesMixin, UserSuccessUrl, UpdateView):
    """Изменение профиля пользователя"""

    model = User
    fields = (
        'username', 'first_name', 'last_name', 'email'
    )
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user


class AddCommentCreateView(UserPassesMixin, PostSuccessUrl, CreateView):
    # UserPassesMixin
    """Добавление коментариев"""

    model = Comments
    fields = ('text',)
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post,
            pk=self.kwargs['post_id']
        )
        return super().form_valid(form)


class EditCommentUpdateView(
    UserPassesMixin, OnlyAuthorMixin, PostSuccessUrl, UpdateView
):
    """Измененить коментарий"""

    model = Comments
    template_name = 'blog/comment.html'
    form_class = AddPostForm
    pk_url_kwarg = 'comment_id'
    context_object_name = 'comment'

    def get_queryset(self):
        result = super().get_queryset().filter(
            pk=self.kwargs['comment_id'],
        ).order_by('created_at',)
        return result


class ComentDeleteView(
    UserPassesMixin, OnlyAuthorMixin, PostSuccessUrl, DeleteView
):
    """Удаление коментария"""

    model = Comments
    template_name = 'blog/comment.html'
    form_class = AddPostForm
    pk_url_kwarg = 'comment_id'
    context_object_name = 'comment'

    def get_queryset(self):
        result = super().get_queryset().filter(
            pk=self.kwargs['comment_id'],
        ).order_by('created_at',)
        return result
