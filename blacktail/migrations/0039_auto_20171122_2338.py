# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 23:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blacktail', '0038_auto_20171122_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storiespage',
            name='dossier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blacktail.StoryDossier'),
        ),
    ]
