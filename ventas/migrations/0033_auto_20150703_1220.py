# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0032_auto_20150703_1215'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='turno',
            unique_together=set([]),
        ),
    ]
