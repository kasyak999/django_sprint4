from django import forms
from .models import Post, Comment


class FormComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'text',
        )


class AddForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('is_published', 'author')
        widgets = {
            # 'pub_date': forms.DateInput(attrs={'type': 'date'}),
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
