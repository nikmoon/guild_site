# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('msgCreated', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('msgLastChanged', models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')),
                ('msgText', models.TextField(blank=True, default='', verbose_name='текст сообщения')),
                ('msgAuthor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
