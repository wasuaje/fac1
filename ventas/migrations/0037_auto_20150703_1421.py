# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ventas', '0036_auto_20150703_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='caja',
            field=models.ForeignKey(to='ventas.Caja', null=True),
        ),
        migrations.AddField(
            model_name='turno',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
