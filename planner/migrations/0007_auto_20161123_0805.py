# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0006_auto_20161116_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawn',
            name='size',
            field=models.IntegerField(),
        ),
    ]
