# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-23 02:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0010_auto_20170107_2127'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grasstype',
            options={'ordering': ['season', 'name']},
        ),
        migrations.RemoveField(
            model_name='lawn',
            name='grass_type',
        ),
    ]
