# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 01:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawn',
            name='size',
            field=models.IntegerField(default=0),
        ),
    ]
