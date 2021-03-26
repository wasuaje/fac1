# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0017_cuentabanco'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipocaja',
            name='codigo',
            field=models.CharField(max_length=5, null=True, blank=True),
        ),
    ]
