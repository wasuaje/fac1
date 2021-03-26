# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0018_auto_20150622_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='caja',
            name='tipocaja',
            field=models.ForeignKey(to='ventas.TipoCaja', null=True),
        ),
    ]
