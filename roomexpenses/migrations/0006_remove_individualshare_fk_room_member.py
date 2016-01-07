# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0005_auto_20160107_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individualshare',
            name='fk_room_member',
        ),
    ]
