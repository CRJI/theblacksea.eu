# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-17 11:27
from __future__ import unicode_literals

import blacktail.models.streamfield
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blacktail', '0055_auto_20180517_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='body',
            field=wagtail.core.fields.StreamField((('header', wagtail.core.blocks.StructBlock((('h1', wagtail.core.blocks.TextBlock('h1')), ('h2', wagtail.core.blocks.TextBlock('h2')), ('h3', wagtail.core.blocks.TextBlock('h3')), ('h4', wagtail.core.blocks.TextBlock('h4')), ('image', wagtail.images.blocks.ImageChooserBlock())))), ('h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('aligned_image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock()), ('alignment', blacktail.models.streamfield.ImageFormatChoiceBlock())), icon='image', label='Aligned image')), ('pullquote', wagtail.core.blocks.StructBlock((('quote', wagtail.core.blocks.TextBlock('quote title')), ('attribution', wagtail.core.blocks.CharBlock())))), ('aligned_html', wagtail.core.blocks.StructBlock((('html', wagtail.core.blocks.RawHTMLBlock()), ('alignment', blacktail.models.streamfield.HTMLAlignmentChoiceBlock())), icon='code', label='Raw HTML')), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse'))), blank=True),
        ),
    ]
