# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-22 12:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailimages', '0019_delete_filter'),
        ('wagtailcore', '0040_page_draft_title'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('taggit', '0002_auto_20150616_2121'),
        ('blacktail', '0047_auto_20180322_1112'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoriesFolder',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('date', models.DateField(verbose_name='Post date')),
                ('intro', models.CharField(blank=True, max_length=1000)),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('feed_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stories_folder_related', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='StoriesFolderTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='blacktail.StoriesFolder')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacktail_storiesfoldertag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='storyfolder',
            name='feed_image',
        ),
        migrations.RemoveField(
            model_name='storyfolder',
            name='image',
        ),
        migrations.RemoveField(
            model_name='storyfolder',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='storyfolder',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='storyfoldertag',
            name='content_object',
        ),
        migrations.RemoveField(
            model_name='storyfoldertag',
            name='tag',
        ),
        migrations.DeleteModel(
            name='StoryFolder',
        ),
        migrations.DeleteModel(
            name='StoryFolderTag',
        ),
        migrations.AddField(
            model_name='storiesfolder',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blacktail.StoriesFolderTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
