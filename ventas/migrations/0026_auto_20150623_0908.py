# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0025_auto_20150622_1717'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='turno',
            unique_together=set([('usuario', 'caja')]),
        ),
    ]
