from django import forms
from .models import Post, Comment, User


class FormUserComment(forms.ModelForm):
    """Форма редактирования пользователя."""

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email'
        )


class FormComment(forms.ModelForm):
    """Форма создания коментария."""

    class Meta:
        model = Comment
        fields = (
            'text',
        )


class PostCreationForm(forms.ModelForm):
    """Форма создания поста."""

    class Meta:
        model = Post
        exclude = ('is_published', 'author')
        widgets = {
            # 'pub_date': forms.DateInput(attrs={'type': 'date'}),
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
