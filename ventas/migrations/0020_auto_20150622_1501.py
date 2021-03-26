# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0019_caja_tipocaja'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='fecha_hora_fin',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, blank=True),
        ),
    ]
