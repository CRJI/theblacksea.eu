# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-17 12:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('blacktail', '0009_auto_20171016_1500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True)),
                ('text', models.CharField(max_length=255)),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adverts', to='wagtailcore.Page')),
            ],
        ),
        migrations.CreateModel(
            name='AdvertPlacement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blacktail.Advert')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='advert_placements', to='wagtailcore.Page')),
            ],
        ),
    ]
