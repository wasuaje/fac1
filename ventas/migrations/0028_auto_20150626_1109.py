# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0027_turnodet_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='formapago',
            name='efectivo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='formapago',
            name='monetizable',
            field=models.BooleanField(default=True),
        ),
    ]
