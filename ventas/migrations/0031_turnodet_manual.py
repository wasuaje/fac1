# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0030_auto_20150626_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='turnodet',
            name='manual',
            field=models.BooleanField(default=False),
        ),
    ]
