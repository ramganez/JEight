# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adjustmentfrompeople',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='individualshare',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='monthexpense',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='monthinvestment',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
