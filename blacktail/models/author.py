from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailsearch import index

from wagtail.wagtailcore.blocks import StructBlock, StreamBlock, FieldBlock, \
    CharBlock, RichTextBlock, RawHTMLBlock, ChooserBlock

from modelcluster.fields import ParentalManyToManyField


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

    search_fields = Page.search_fields + [
        index.SearchField('bio'),
        index.SearchField('occupation'),
    ]

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
