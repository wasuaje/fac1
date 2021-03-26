# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0015_auto_20150622_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoCaja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=2, null=True, blank=True)),
                ('nombre', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'tipo_caja',
            },
        ),
    ]
