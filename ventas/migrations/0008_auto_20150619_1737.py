# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0007_auto_20150619_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='TurnoDet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('ingreso', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('egreso', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
            ],
            options={
                'db_table': 'turno_det',
            },
        ),
        migrations.RenameField(
            model_name='caja',
            old_name='tot_egresos',
            new_name='egresos',
        ),
        migrations.RenameField(
            model_name='caja',
            old_name='tot_ingresos',
            new_name='ingresos',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='egreso',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='ingreso',
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_hora_fin',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AddField(
            model_name='turnodet',
            name='turno',
            field=models.ForeignKey(to='ventas.Turno'),
        ),
    ]
