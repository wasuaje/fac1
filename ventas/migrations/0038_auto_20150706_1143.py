# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0037_auto_20150703_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='caja',
            name='saldo_apertura',
            field=models.DecimalField(default=0.0, max_digits=9, decimal_places=2),
        ),
        migrations.AddField(
            model_name='caja',
            name='saldo_cierre',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True),
        ),
    ]
