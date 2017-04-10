from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape
import json

# Create your models here.


class ChatMessage(models.Model):
    msgCreated = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    msgLastChanged = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')
    msgText = models.TextField(blank=True, default='', verbose_name='текст сообщения')
    msgAuthor = models.ForeignKey(User)

    def to_dict(self):
        return {
            'id': self.id,
            'created': self.msgCreated.strftime("%c"),
            'lastChanged': self.msgLastChanged.strftime("%c"),
            'text': escape(self.msgText),
            'author': escape(self.msgAuthor.username),
        }
