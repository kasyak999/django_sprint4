
from django.shortcuts import get_object_or_404
from blog.models import Post, Category, User, Comment
from django.utils import timezone
from django.views.generic import (
    DetailView, UpdateView, ListView, CreateView, DeleteView
)
from django.urls import reverse, reverse_lazy
from .forms import FormComment, PostCreationForm, FormUserComment
from django.db.models import Count
from .mixin import OnlyAuthorMixin, CommentMixin
from django.contrib.auth.mixins import LoginRequiredMixin


OBJECTS_PER_PAGE = 10


class IndexListView(ListView):
    """Главная страница"""

    model = Post
    template_name = 'blog/index.html'
    paginate_by = OBJECTS_PER_PAGE
    context_object_name = 'page_obj'

    def get_queryset(self):
        return self.model.objects.main_filter()


class CategoryPostsListView(ListView):  # DetailView
    """Вывод постов в категории"""

    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = OBJECTS_PER_PAGE

    def get_queryset(self):
        category = get_object_or_404(
            super().get_queryset(),
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        result = category.posts.filter(
            category__slug=self.kwargs['category_slug'],
            is_published=True,
            pub_date__lt=timezone.now()
        )
        return result.select_related(
            'author', 'category', 'location'
        ).annotate(
            comment_count=Count('comment')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            self.model,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return context


class PostDetail(DetailView):
    """Пост подробнее"""

    model = Post
    template_name = 'blog/detail.html'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author', 'category', 'location'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = (
            context['post'].comment.all().select_related('author')
        )
        context['form'] = FormComment()
        return context

    def get_object(self, queryset=None):
        post = super().get_object()
        if post.author == self.request.user:
            return post
        return get_object_or_404(
            self.get_queryset(), is_published=True,
            category__is_published=True,
            pub_date__lt=timezone.now(),
            pk=self.kwargs[self.pk_url_kwarg]
        )


class CreatingNewPostView(LoginRequiredMixin, CreateView):
    """Создание нового поста"""

    model = Post
    form_class = PostCreationForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUserDeleteView(LoginRequiredMixin, OnlyAuthorMixin, DeleteView):
    """Удаление поста"""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostCreationForm(instance=self.object)
        return context

    def get_queryset(self):
        result = super().get_queryset().filter(
            pk=self.kwargs['post_id'],
        ).order_by('created_at',)
        return result


class PostUpdateView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    """Измененить пост пользователя"""

    model = Post
    form_class = PostCreationForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        result = super().get_queryset().filter(
            pk=self.kwargs['post_id'],
        ).order_by('created_at',)
        return result

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )


class ProfileDetailView(ListView):
    """Просмотреть профиль пользователя"""

    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'username'
    paginate_by = OBJECTS_PER_PAGE

    def get_queryset(self):
        self.user = get_object_or_404(
            User,
            username=self.kwargs[self.pk_url_kwarg]
        )
        if self.user == self.request.user:
            queryset = Post.objects.filter(
                author=self.user
            )
        else:
            queryset = Post.objects.main_filter().filter(
                author=self.user
            )
        return queryset.select_related(
            'author', 'category', 'location'
        ).annotate(comment_count=Count('comment')).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение профиля пользователя"""

    model = User
    form_class = FormUserComment
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class AddCommentCreateView(LoginRequiredMixin, CreateView):
    """Добавление коментариев"""

    model = Comment
    fields = ('text',)
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post,
            is_published=True,
            category__is_published=True,
            pk=self.kwargs['post_id']
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )


class EditCommentUpdateView(
    LoginRequiredMixin, OnlyAuthorMixin, CommentMixin, UpdateView
):
    """Измененить коментарий"""


class CommentDeleteView(
    LoginRequiredMixin, OnlyAuthorMixin, CommentMixin, DeleteView
):
    """Удаление коментария"""
