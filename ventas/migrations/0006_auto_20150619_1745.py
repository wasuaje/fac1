# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_auto_20150619_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cobros',
            name='estado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='documento',
            name='estado',
            field=models.BooleanField(default=False),
        ),
    ]
