from django.db import models

# Create your models here.

from django.db import models
from django.template.backends import django


class user(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=150)
    profile = models.CharField(max_length=250)
    token = models.CharField(max_length=256)
    token_time = models.DateTimeField()



    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)