from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
# get_list_or_404
from django.http import HttpResponse, HttpRequest
from blog.models import Post, Category, User
from django.utils import timezone

from django.views.generic import DetailView, UpdateView, ListView, CreateView
from django.urls import reverse_lazy

from django.core.paginator import Paginator
from django.db.models import Q


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
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        return self.request.user


class IndexListView(ListView):
    """Главная страница"""

    queryset = Post.objects.main_filter()
    template_name = 'blog/index.html'
    paginate_by = 10
    context_object_name = 'post_list'


class CreateCreateView(CreateView):
    """Создание нового поста"""

    model = Post
    fields = (
        'title', 'text', 'pub_date', 'category', 'location'
    )
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


class PostUpdateView(UpdateView):
    """Изменение поста пользователя"""

    model = Post
    fields = (
        'title', 'text', 'pub_date', 'category', 'location'
    )
    template_name = 'blog/user.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return super().get_queryset().filter(
            pk=self.kwargs['post_id'], author=self.request.user
        )

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )

    # def handle_no_permission(self):
    #     return redirect('blog:index')


class CategoryPostsListView(ListView):
    """Вывод постов в категории"""

    context_object_name = 'post_list'
    template_name = 'blog/category.html'
    paginate_by = 10

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
