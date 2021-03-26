# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0039_auto_20150707_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='cantidad',
            field=models.BigIntegerField(default=1),
        ),
    ]
