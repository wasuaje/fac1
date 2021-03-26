# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0028_auto_20150626_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='monto_apertura',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='turno',
            name='monto_cierre',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True),
        ),
    ]
