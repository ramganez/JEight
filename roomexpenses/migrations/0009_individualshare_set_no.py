# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0008_auto_20160107_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualshare',
            name='set_no',
            field=models.IntegerField(default=0, max_length=7),
        ),
    ]
