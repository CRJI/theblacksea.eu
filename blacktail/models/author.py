from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


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

    def story_url(self):
        if self.image:
            return f"/about/author/{self.id}"
        elif self.url:
            return self.url
        else:
            return "#"

    def stories(self):
        from .stories import Story
        return (
            Story.objects
            .filter(author_ids__contains=self.pk)
            .order_by('-first_published_at')
        )

    def blogs(self):
        from .blog import BlogPost
        return (
            BlogPost.objects
            .filter(author_ids__contains=self.pk)
            .order_by('-first_published_at')
        )
