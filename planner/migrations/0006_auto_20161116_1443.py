# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0005_auto_20161108_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weatherstation',
            name='id',
        ),
        migrations.AlterField(
            model_name='weatherstation',
            name='stationid',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
