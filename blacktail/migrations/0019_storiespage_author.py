# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 13:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blacktail', '0018_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='storiespage',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blacktail.Author'),
        ),
    ]
