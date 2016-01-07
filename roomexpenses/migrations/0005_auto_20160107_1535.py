# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0004_auto_20160106_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualshare',
            name='shared',
            field=models.CharField(default=0, max_length=10, choices=[(0, b'All'), (1, b'Rent Only'), (2, b'Food Only')]),
        ),
    ]
