# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0006_remove_individualshare_fk_room_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individualshare',
            name='fk_afp',
        ),
        migrations.AddField(
            model_name='individualshare',
            name='fk_room_member',
            field=models.OneToOneField(null=True, blank=True, to='roomexpenses.RoomMember'),
        ),
    ]
