# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0002_remove_documento_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='estado',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
