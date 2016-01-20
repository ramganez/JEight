# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
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
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IndividualShare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('shared', models.IntegerField(default=0, choices=[(0, b'All'), (1, b'Rent Only'), (2, b'Food Only')])),
                ('amount_to_pay', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('set_unique_no', models.CharField(default=0, max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MonthExpense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('rent', models.DecimalField(default=8000, max_digits=7, decimal_places=2)),
                ('maintenance', models.DecimalField(default=300, max_digits=7, decimal_places=2)),
                ('cable', models.DecimalField(default=150, max_digits=7, decimal_places=2)),
                ('EB', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('water', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('commonEB', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('veg_shop', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('other', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MonthInvestment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('provision_store', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('new_things', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('gas', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('rice_bag', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoomMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=12)),
                ('mail_id', models.EmailField(max_length=75)),
                ('advance_given', models.DecimalField(max_digits=6, decimal_places=2)),
                ('other_exp_paid', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='individualshare',
            name='fk_room_member',
            field=models.ForeignKey(blank=True, to='roomexpenses.RoomMember', null=True),
        ),
        migrations.AddField(
            model_name='adjustmentfrompeople',
            name='fk_investment',
            field=models.ForeignKey(to='roomexpenses.MonthInvestment'),
        ),
    ]
