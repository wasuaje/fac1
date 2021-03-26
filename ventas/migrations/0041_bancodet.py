# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0040_auto_20150708_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='BancoDet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100, null=True, blank=True)),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('ingreso', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('egreso', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('manual', models.NullBooleanField(default=False)),
                ('cuentabanco', models.ForeignKey(to='ventas.CuentaBanco')),
            ],
            options={
                'db_table': 'banco_det',
            },
        ),
    ]
