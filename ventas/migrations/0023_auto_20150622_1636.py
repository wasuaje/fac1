# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0022_auto_20150622_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='fecha',
            field=models.DateField(default=datetime.datetime.now, blank=True),
        ),
    ]
