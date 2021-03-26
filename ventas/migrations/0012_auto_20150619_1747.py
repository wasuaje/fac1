# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0011_auto_20150619_1746'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehiculo',
            old_name='kilometraje',
            new_name='kilometraje1',
        ),
    ]
