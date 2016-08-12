# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('happiness', '0004_happiness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='happiness',
            name='date',
            field=models.DateField(),
        ),
    ]
