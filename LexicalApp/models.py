from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    book = models.FileField(upload_to='library/')

