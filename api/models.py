from django.db import models
from core.models import Article


class Mark(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    users_liked = models.JSONField()
    users_disliked = models.JSONField()


class Comment(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    comments = models.JSONField()
