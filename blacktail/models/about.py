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

from .author import Author

class AboutPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        FieldPanel('body', classname='full'),
    ]


class AuthorPage(Page):
    intro = RichTextField(blank=True)
    image = models.ImageField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        FieldPanel('image'),
    ]

    def get_context(self, request):

        # Update context
        context = super(AuthorPage, self).get_context(request)
        author_id = request.path.strip('/').split('/')[-1]

        author_found = Author.objects.get(pk=author_id)
        context['model'] = author_found

        return context

    def route(self, request, path_components):
        if path_components:
            # request is for an author
            author_id = path_components[0]

            # find a matching author or 404
            try:
                author_found = Author.objects.get(pk=author_id)
            except Page.DoesNotExist:
                raise Http404
        else:
            # the page matches the request, but has no author id
            raise Http404

        if self.live:
            # Return a RouteResult that will tell Wagtail to call
            # this page's serve() method
            return RouteResult(self)
        else:
            # the page matches the request, but isn't published, so 404
            raise Http404
