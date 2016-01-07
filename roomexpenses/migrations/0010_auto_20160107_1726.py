# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0009_individualshare_set_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individualshare',
            name='set_no',
        ),
        migrations.AddField(
            model_name='individualshare',
            name='set_unique_no',
            field=models.CharField(default=b'4268188d8811453f9e741d4e19af1246', max_length=32),
        ),
    ]
