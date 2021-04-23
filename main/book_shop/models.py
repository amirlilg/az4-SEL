from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256, unique=True)
    category = models.CharField(max_length=256)
    authors = models.CharField(max_length=256)
