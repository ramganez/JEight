# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('roomexpenses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdjustmentFromPeople',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('people_name', models.CharField(max_length=50)),
                ('amount', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('fk_invesment', models.ForeignKey(to='roomexpenses.MonthInvesment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
