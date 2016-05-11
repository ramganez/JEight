# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0002_auto_20160328_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthinvestment',
            name='last_month_bal',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=2),
        ),
    ]
