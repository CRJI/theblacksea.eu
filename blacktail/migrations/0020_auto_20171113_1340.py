# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 13:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blacktail', '0019_storiespage_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoriesAuthors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(max_length=100)),
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.RemoveField(
            model_name='storiespage',
            name='author',
        ),
        migrations.RemoveField(
            model_name='storiespage',
            name='authors',
        ),
        migrations.AddField(
            model_name='storiesauthors',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='blacktail.StoriesPage'),
        ),
    ]
