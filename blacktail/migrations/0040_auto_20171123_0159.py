# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 01:59
from __future__ import unicode_literals

import blacktail.models
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0040_page_draft_title'),
        ('taggit', '0002_auto_20150616_2121'),
        ('blacktail', '0039_auto_20171122_2338'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('date', models.DateField(verbose_name='Post date')),
                ('intro', models.CharField(blank=True, max_length=255)),
                ('body_richtext', wagtail.core.fields.RichTextField(blank=True)),
                ('body_blocks', wagtail.core.fields.StreamField((('h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('aligned_image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock()), ('alignment', blacktail.models.ImageFormatChoiceBlock())), icon='image', label='Aligned image')), ('pullquote', wagtail.core.blocks.StructBlock((('quote', wagtail.core.blocks.TextBlock('quote title')), ('attribution', wagtail.core.blocks.CharBlock())))), ('aligned_html', wagtail.core.blocks.StructBlock((('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', blacktail.models.HTMLAlignmentChoiceBlock())), icon='code', label='Raw HTML')), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse'))), blank=True)),
                ('format', models.CharField(blank=True, max_length=50)),
                ('authors', modelcluster.fields.ParentalManyToManyField(related_name='stories', to='blacktail.Author')),
                ('dossier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blacktail.StoryDossier')),
                ('feed_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stories_related', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='StoryPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='blacktail.StoryPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacktail_storypagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='StoriesPageLocation',
            new_name='StoryPageLocation',
        ),
        migrations.RemoveField(
            model_name='storiespage',
            name='authors',
        ),
        migrations.RemoveField(
            model_name='storiespage',
            name='dossier',
        ),
        migrations.RemoveField(
            model_name='storiespage',
            name='feed_image',
        ),
        migrations.RemoveField(
            model_name='storiespage',
            name='image',
        ),
        migrations.RemoveField(
            model_name='storiespage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='storiespage',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='storiespage',
            name='type',
        ),
        migrations.RemoveField(
            model_name='storiespagetag',
            name='content_object',
        ),
        migrations.RemoveField(
            model_name='storiespagetag',
            name='tag',
        ),
        migrations.AlterField(
            model_name='storypagelocation',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='blacktail.StoryPage'),
        ),
        migrations.DeleteModel(
            name='StoriesPage',
        ),
        migrations.DeleteModel(
            name='StoriesPageTag',
        ),
        migrations.AddField(
            model_name='storypage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blacktail.StoryPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='storypage',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blacktail.StoryType'),
        ),
    ]
