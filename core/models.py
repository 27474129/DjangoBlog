from django.db import models
from django.core.exceptions import ValidationError
from random import randint


class Article(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    content = models.TextField()
    who_uploaded = models.CharField(max_length=105, null=True)
    is_published = models.BooleanField(default=False)
    publication_time = models.DateTimeField(null=True)
    slug = models.SlugField(unique=True, null=True)
