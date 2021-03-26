# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0012_auto_20150619_1747'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehiculo',
            old_name='kilometraje1',
            new_name='kilometraje',
        ),
    ]
