# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-29 10:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170929_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storiespage',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
