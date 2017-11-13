# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 13:21
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_storiespage_feed_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('intro', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
            ],
        ),
    ]
