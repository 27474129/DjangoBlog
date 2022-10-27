from django import forms
from .models import Article
from django.core.exceptions import ValidationError


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "photo", "content", "who_uploaded", "slug"]
