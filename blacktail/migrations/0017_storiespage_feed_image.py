# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 11:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('blacktail', '0016_auto_20171030_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='storiespage',
            name='feed_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
