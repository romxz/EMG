# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('happiness', '0008_auto_20160123_2300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='happiness',
            options={'ordering': ['date'], 'get_latest_by': 'date'},
        ),
        migrations.AlterUniqueTogether(
            name='happiness',
            unique_together=set([('employee', 'date')]),
        ),
    ]
