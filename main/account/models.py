import django
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    profile = models.CharField(max_length=512)
    token = models.CharField(max_length=256)
    token_expire = models.DateTimeField(default=django.utils.timezone.now)
    isAdmin = models.BooleanField(default=False)
