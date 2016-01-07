# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0010_auto_20160107_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualshare',
            name='set_unique_no',
            field=models.CharField(default=b'4fcfe7a1143a4eca9b62a44d0b2b98c3', max_length=32),
        ),
        migrations.AlterField(
            model_name='individualshare',
            name='shared',
            field=models.IntegerField(default=0, choices=[(0, b'All'), (1, b'Rent Only'), (2, b'Food Only')]),
        ),
    ]
