from django.db import models
from django.contrib.auth.models import User


class NewsItem(models.Model):
    was_created = models.DateTimeField('дата создания', auto_now_add=True)
    author = models.ForeignKey(User, verbose_name='автор новости')
    title = models.CharField(max_length=300, verbose_name='заголовок новости')
    text = models.TextField(verbose_name='текст новости')

