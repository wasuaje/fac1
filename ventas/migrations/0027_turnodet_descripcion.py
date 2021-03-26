# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0026_auto_20150623_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='turnodet',
            name='descripcion',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
