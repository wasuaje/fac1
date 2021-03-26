# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0031_turnodet_manual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='saldo_apertura',
            field=models.DecimalField(default=0.0, max_digits=9, decimal_places=2),
        ),
    ]
