# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0021_auto_20150622_1502'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='caja',
            unique_together=set([('tipocaja', 'fecha')]),
        ),
    ]
