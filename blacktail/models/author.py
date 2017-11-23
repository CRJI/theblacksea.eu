from __future__ import absolute_import, unicode_literals
from datetime import date
from itertools import chain
from operator import attrgetter

from django.db import models
from django.shortcuts import render
from django.http.response import Http404
from django.utils.encoding import python_2_unicode_compatible
from django import forms

from wagtail.wagtailcore.url_routing import RouteResult
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel

from wagtail.wagtailsearch import index

from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, \
    CharBlock, RichTextBlock, RawHTMLBlock, ChooserBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase


class Author(models.Model):
    name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100, blank=True)
    bio = RichTextField(blank=True)
    url = models.URLField(max_length=254, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('occupation'),
        ]),
        FieldPanel('bio'),
        MultiFieldPanel([
            FieldPanel('url'),
            FieldPanel('email'),
        ]),
        ImageChooserPanel('image'),
    ]
    def __str__(self):
        return "%s" % (self.name)
