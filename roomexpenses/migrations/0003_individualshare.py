# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0002_adjustmentfrompeople'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndividualShare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('shared', models.CharField(default=b'All', max_length=10)),
                ('amount_to_pay', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('fk_afp', models.ForeignKey(to='roomexpenses.AdjustmentFromPeople')),
                ('fk_room_member', models.OneToOneField(to='roomexpenses.RoomMember')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
