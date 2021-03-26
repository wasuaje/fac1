# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0016_tipocaja'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuentaBanco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=20, null=True, blank=True)),
                ('contacto', models.CharField(max_length=100, null=True, blank=True)),
                ('banco', models.ForeignKey(to='ventas.Banco')),
            ],
            options={
                'db_table': 'cuenta_banco',
            },
        ),
    ]
