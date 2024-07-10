from django import forms
from .models import Post


class MainForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class AddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'text', 'pub_date', 'category', 'location', 'image'
        )
        widgets = {
            # 'pub_date': forms.DateInput(attrs={'type': 'date'}),
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
