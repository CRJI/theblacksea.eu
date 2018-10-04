from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, \
    TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase


class BlogIndex(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(BlogIndex, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['posts'] = blogpages
        return context

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('color'),
        ]),
    ]

    def __str__(self):
        return "%s" % (self.name)

class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('blacktail.BlogPost', related_name='tagged_items')

class BlogPost(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    authors = ParentalManyToManyField('Author', related_name='blogs')

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('image'),
            FieldPanel('authors'),
            FieldPanel('first_published_at'),
            FieldPanel('category'),
        ]),
        FieldPanel('intro', classname='full'),
        FieldPanel('body', classname='full'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])
