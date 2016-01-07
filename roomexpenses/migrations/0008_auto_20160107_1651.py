# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0007_auto_20160107_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualshare',
            name='fk_room_member',
            field=models.ForeignKey(blank=True, to='roomexpenses.RoomMember', null=True),
        ),
    ]
