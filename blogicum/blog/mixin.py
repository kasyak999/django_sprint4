from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class UserSuccessUrl():
    """Перенаправление на страницк пользователя"""

    def get_success_url(self):
        return reverse(
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
