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
            name='NewsItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('was_created', models.DateTimeField(verbose_name='дата создания', auto_now_add=True)),
                ('title', models.CharField(verbose_name='заголовок новости', max_length=300)),
                ('text', models.TextField(verbose_name='текст новости')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='автор новости')),
            ],
        ),
    ]
