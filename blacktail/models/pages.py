from __future__ import absolute_import, unicode_literals
from itertools import chain
from operator import attrgetter

from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.search import index

from .stories import Story
from .blog import BlogPost


class HomePage(Page):
    body = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('image')
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)

        # Add extra variables and return the updated context
        blogs = BlogPost.objects.live().order_by('-first_published_at').reverse()[:8]
        stories = Story.objects.live().order_by('-first_published_at').reverse()[:8]

        context['all_posts'] = sorted(
            chain(blogs, stories),
            key=attrgetter('date'))
        context['blogs'] = blogs
        context['stories'] = stories
        return context

class StaticPage(Page):
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full')
    ]
