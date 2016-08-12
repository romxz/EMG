# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('happiness', '0002_auto_20151210_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='manager',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
