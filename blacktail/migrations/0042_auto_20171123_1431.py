# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 14:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blacktail', '0041_auto_20171123_0213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='body_blocks',
            new_name='body',
        ),
        migrations.RemoveField(
            model_name='story',
            name='body_richtext',
        ),
    ]
