# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-04 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blacktail', '0069_auto_20180910_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='summary',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
