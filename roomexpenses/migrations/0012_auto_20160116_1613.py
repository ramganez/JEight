# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0011_auto_20160107_1854'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MonthInvesment',
            new_name='MonthInvestment',
        ),
        migrations.RenameField(
            model_name='adjustmentfrompeople',
            old_name='fk_invesment',
            new_name='fk_investment',
        ),
        migrations.AlterField(
            model_name='individualshare',
            name='set_unique_no',
            field=models.CharField(default=b'0592e8ecf32d4fbbb1fc3ecfcf0702f8', max_length=32),
        ),
    ]
