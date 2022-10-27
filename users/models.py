from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=255)
    secondname = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.TextField()

    class Meta:
        app_label = 'users'

    