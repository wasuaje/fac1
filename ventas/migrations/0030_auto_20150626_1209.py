# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0029_auto_20150626_1155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='turno',
            old_name='monto_apertura',
            new_name='saldo_apertura',
        ),
        migrations.RenameField(
            model_name='turno',
            old_name='monto_cierre',
            new_name='saldo_cierre',
        ),
    ]
