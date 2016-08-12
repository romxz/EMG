# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('happiness', '0007_usersession'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersession',
            name='bokeh_session_individual',
        ),
        migrations.RemoveField(
            model_name='usersession',
            name='bokeh_session_individuals',
        ),
        migrations.RemoveField(
            model_name='usersession',
            name='bokeh_session_team',
        ),
        migrations.RemoveField(
            model_name='usersession',
            name='bokeh_session_teams',
        ),
        migrations.AddField(
            model_name='usersession',
            name='bokeh_session_id',
            field=models.CharField(max_length=64, default=None),
            preserve_default=False,
        ),
    ]
