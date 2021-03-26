# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0008_auto_20150619_1737'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='caja',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='turnodet',
            options={'managed': False},
        ),
    ]
