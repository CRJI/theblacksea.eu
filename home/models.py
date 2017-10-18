from __future__ import absolute_import, unicode_literals
from itertools import chain
from operator import attrgetter

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from blog import models as TBSModels


class HomePage(Page):
    body = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('image')
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)

        # Add extra variables and return the updated context
        blog_list = TBSModels.BlogPage.objects.live()
        story_list = TBSModels.StoriesPage.objects.live()
        context['all_posts'] = sorted(
            chain(blog_list, story_list),
            key=attrgetter('date'))
        return context

class StaticPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full')
    ]
