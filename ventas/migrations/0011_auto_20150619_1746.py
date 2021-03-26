# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0010_auto_20150619_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caja',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='caja',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='turnodet',
            name='turno',
        ),
        migrations.DeleteModel(
            name='Caja',
        ),
        migrations.DeleteModel(
            name='Turno',
        ),
        migrations.DeleteModel(
            name='TurnoDet',
        ),
    ]
