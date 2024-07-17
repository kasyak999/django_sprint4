from django.shortcuts import redirect
from .forms import FormComment
from django.urls import reverse
from blog.models import Comment


class OnlyAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            return redirect(
                'blog:post_detail', kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    form_class = FormComment
    pk_url_kwarg = 'comment_id'
    context_object_name = 'comment'

    def get_queryset(self):
        result = super().get_queryset().filter(
            pk=self.kwargs['comment_id'],
        ).order_by('created_at',)
        return result

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )
