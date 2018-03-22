from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    InlinePanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

from .streamfield import BlogStreamBlock

class Location(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
    ]

    class Meta:
        abstract = True

class StoryLocation(Orderable, Location):
    page = ParentalKey('blacktail.Story', related_name='locations')

class StoryTemplate(models.Model):
    name = models.CharField(max_length=100)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return "%s" % (self.name)

class StoryType(models.Model):
    name = models.CharField(max_length=100)
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
            ImageChooserPanel('image'),
        ]),
    ]

    def __str__(self):
        return "%s" % (self.name)

class StoryDossier(models.Model):
    name = models.CharField(max_length=100)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return "%s" % (self.name)

class StoryTag(TaggedItemBase):
    content_object = ParentalKey('blacktail.Story', related_name='tagged_items')
class StoryFolderTag(TaggedItemBase):
    content_object = ParentalKey('blacktail.StoryFolder', related_name='tagged_items')

class StoriesIndex(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]

    # def serve(self, request):
    #     # Get stories
    #     stories = self.get_children().live().order_by('-first_published_at')

    #     return render(request, self.template, {
    #         'page': self,
    #         'stories': stories,
    #     })

    def get_context(self, request):

        # Update context to include only published posts, ordered by reverse-chron
        context = super(StoriesIndex, self).get_context(request)
        stories = self.get_children().live().order_by('-first_published_at')
        context['stories'] = stories

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            stories = stories.filter(tags__name=tag)

        return context

class Story(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=1000, blank=True)
    body = StreamField(BlogStreamBlock(), blank=True)
    # location = models.CharField(max_length=255, blank=True)

    dossier = models.CharField(max_length=50, blank=True)
    format = models.CharField(max_length=50, blank=True)
    tags = ClusterTaggableManager(through=StoryTag, blank=True)
    # authors = ChooserBlock(target_model=Author, blank=True)
    # authors = models.ForeignKey(
    #     'blacktail.Author',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='stories'
    # )
    # authors = models.ManyToManyField(Author)
    authors = ParentalManyToManyField('Author', related_name='stories')
    type = models.ForeignKey(StoryType, on_delete=models.SET_NULL, blank=True, null=True)
    post_template = models.ForeignKey(StoryTemplate, on_delete=models.SET_NULL, blank=True, null=True)
    dossier = models.ForeignKey(StoryDossier, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='stories_related'
    )
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # template = models.ForeignKey('blacktail.BlogTemplate')

    @property
    def stories_index(self):
        # Find closest ancestor which is a blog index
        return self.get_ancestors().type(StoriesIndex).last()

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        # index.SearchField('location'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        ImageChooserPanel('image'),
        # InlinePanel('page_authors'),
        MultiFieldPanel([
            FieldPanel('authors'),
            FieldPanel('type'),
            FieldPanel('dossier'),
            FieldPanel('date'),
            # FieldPanel('location'),
        ]),
        InlinePanel('locations', label="Locations"),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('feed_image'),
        FieldPanel('tags'),
    ]

    blocks_panels = [
        StreamFieldPanel('body', classname='full'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content details'),
        ObjectList(blocks_panels, heading='Content'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


class StoryFolder(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=1000, blank=True)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=StoryFolderTag, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='story_folder_related'
    )
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        # index.SearchField('location'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        ImageChooserPanel('image'),
        FieldPanel('date'),
        FieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('feed_image'),
        FieldPanel('tags'),
    ]
