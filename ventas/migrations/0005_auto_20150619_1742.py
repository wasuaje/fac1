# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0004_auto_20150619_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documento',
            name='status',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='fecha',
        ),
    ]
