# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0006_auto_20150619_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='estado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='turno',
            name='estado',
            field=models.BooleanField(default=False),
        ),
    ]
