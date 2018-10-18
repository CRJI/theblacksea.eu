from __future__ import absolute_import, unicode_literals

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
        blogs = BlogPost.objects.live().order_by('-first_published_at')[:8]
        blog_pairs = [blogs[0:2], blogs[2:4], blogs[4:6], blogs[6:8]]
        stories = Story.objects.live().filter(skip_home__exact=False).filter(translation_for__exact=None).order_by('-first_published_at')[:8]

        context['blog_pairs'] = blog_pairs
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
