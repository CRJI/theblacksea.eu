# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 08:28
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_storiesindexpage_storiespage'),
    ]

    operations = [
        migrations.AddField(
            model_name='storiespage',
            name='location',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='storiespage',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(),
        ),
    ]
