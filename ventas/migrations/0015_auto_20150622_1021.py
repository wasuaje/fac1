# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0014_caja_turno_turnodet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='caja',
            old_name='fecha_hora',
            new_name='fecha_hora_ini',
        ),
        migrations.RenameField(
            model_name='turno',
            old_name='fecha_hora_inicio',
            new_name='fecha_hora_ini',
        ),
        migrations.RemoveField(
            model_name='caja',
            name='egresos',
        ),
        migrations.RemoveField(
            model_name='caja',
            name='ingresos',
        ),
        migrations.RemoveField(
            model_name='caja',
            name='saldo',
        ),
        migrations.AddField(
            model_name='caja',
            name='fecha_hora_fin',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_hora_fin',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
