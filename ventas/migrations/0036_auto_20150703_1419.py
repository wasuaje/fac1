# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0035_auto_20150703_1225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='caja',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='usuario',
        ),
    ]
