from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    firstname = models.CharField(max_length=255)
    secondname = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.TextField()
