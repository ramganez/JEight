# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0003_individualshare'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualshare',
            name='fk_afp',
            field=models.ForeignKey(blank=True, to='roomexpenses.AdjustmentFromPeople', null=True),
        ),
    ]
