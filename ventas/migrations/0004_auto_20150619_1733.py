# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0003_documento_estado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='caja',
            old_name='tota_general',
            new_name='saldo',
        ),
    ]
