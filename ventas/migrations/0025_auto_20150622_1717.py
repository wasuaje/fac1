# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0024_auto_20150622_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='fecha_hora_fin',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
