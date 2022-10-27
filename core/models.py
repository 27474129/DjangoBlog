from django.db import models
from django.core.exceptions import ValidationError
from random import randint


def validate_title_length(title):
    if len(title) < 3:
        raise ValidationError(
            "Название статьи должно содержать минимум 3 символа"
        )


class Article(models.Model):
    title = models.CharField(max_length=255, validators=[validate_title_length])
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    content = models.TextField()
    who_uploaded = models.CharField(max_length=105, null=True)
    is_published = models.BooleanField(default=False)
    publication_time = models.DateTimeField(null=True)
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        app_label = 'core'


class Mark(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    users_liked = models.JSONField()
    users_disliked = models.JSONField()


class Comment(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    comments = models.JSONField()
