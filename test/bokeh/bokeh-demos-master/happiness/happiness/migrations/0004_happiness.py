# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('happiness', '0003_auto_20151210_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Happiness',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('happiness', models.DecimalField(decimal_places=0, max_digits=1)),
                ('employee', models.ForeignKey(to='happiness.Employee')),
            ],
        ),
    ]
