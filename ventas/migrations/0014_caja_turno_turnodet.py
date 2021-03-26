# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ventas', '0013_auto_20150619_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100, null=True, blank=True)),
                ('fecha', models.DateField(default=datetime.datetime.now, unique=True, blank=True)),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('ingresos', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('egresos', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('saldo', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('estado', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'caja',
            },
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100, null=True, blank=True)),
                ('fecha_hora_inicio', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('fecha_hora_fin', models.DateTimeField(blank=True)),
                ('estado', models.BooleanField(default=False)),
                ('caja', models.ForeignKey(to='ventas.Caja')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'turno',
            },
        ),
        migrations.CreateModel(
            name='TurnoDet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('ingreso', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('egreso', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('turno', models.ForeignKey(to='ventas.Turno')),
            ],
            options={
                'db_table': 'turno_det',
            },
        ),
    ]
