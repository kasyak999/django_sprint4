from django.shortcuts import render, get_object_or_404
# get_list_or_404
from django.http import HttpResponse, HttpRequest
from blog.models import Post, Category, User
from django.utils import timezone

from django.views.generic import DetailView, UpdateView, ListView
from django.urls import reverse_lazy


class ProfileDetailView(DetailView):
    """Просмотреть профиль пользователя"""
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'  # Используйте username вместо pk
    slug_url_kwarg = 'username'  # Соответствующее имя в URL
    context_object_name = 'profile'


class ProfileUpdateView(UpdateView):
    """Изменение профиля пользователя"""
    model = User
    fields = (
        'username', 'first_name', 'last_name', 'email'
    )
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        return self.request.user  # Получаем текущего пользователя


class IndexListView(ListView):
    """Главная страница"""
    queryset = Post.objects.main_filter()
    template_name = 'blog/index.html'
    paginate_by = 10
    context_object_name = 'post_list'


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(
        Post.objects.main_filter(),
        id=pk,
    )
    return render(request, 'blog/detail.html', {'post': post})


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
