from __future__ import absolute_import, unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.shortcuts import get_object_or_404

from wagtail.core import hooks
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, \
    InlinePanel, StreamFieldPanel, TabbedInterface, ObjectList, \
    PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.search import index
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

from .streamfield import StoryStreamBlock
from .author import Author
from ..widgets import AuthorsWidget

class RelatedLink(models.Model):
    title = models.CharField(max_length=255)
    link_external = models.URLField("External link", blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('link_external'),
    ]

    class Meta:
        abstract = True

class RelatedPage(models.Model):
    related_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        PageChooserPanel('related_page')
    ]

    class Meta:
        abstract = True

class StoryRelatedLinks(Orderable, RelatedLink):
    page = ParentalKey('blacktail.Story', on_delete=models.CASCADE,
                       related_name='related_links')

class StoryRelatedPages(Orderable, RelatedPage):
    page = ParentalKey('blacktail.Story', on_delete=models.CASCADE,
                       related_name='related_pages')


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
    content_object = ParentalKey('blacktail.Story',
                                 related_name='tagged_items')


class StoriesFolderTag(TaggedItemBase):
    content_object = ParentalKey('blacktail.StoriesFolder',
                                 related_name='tagged_items')


class StoriesFolderTemplate(models.Model):
    name = models.CharField(max_length=100)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return "%s" % (self.name)

class StoriesIndex(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]

    def get_context(self, request):

        # Update context to include only published posts, reverse-chron order
        context = super(StoriesIndex, self).get_context(request)
        stories = Story.objects.live().order_by('-first_published_at')
        tags = Story.tags.filter(
            blacktail_storytag_items__content_object__live=True)
        dossiers = StoryDossier.objects.all()

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            stories = stories.filter(tags__name=tag)

        # Filter by dossier
        dossier_name = request.GET.get('dossier')
        if dossier_name:
            dossier = get_object_or_404(StoryDossier.objects, name=dossier_name)
            stories = stories.filter(dossier=dossier)
        else:
            dossier = None

        context['stories'] = stories
        context['tags'] = tags
        context['dossiers'] = dossiers
        context['selected_dossier'] = dossier

        return context


class Story(Page):
    summary = models.CharField(max_length=1000, blank=True)
    intro = models.CharField(max_length=1000, blank=True)
    body = StreamField(StoryStreamBlock(), blank=True)
    skip_home = models.BooleanField(default=None)
    # location = models.CharField(max_length=255, blank=True)

    translation_language = models.CharField(max_length=2, blank=True)
    translation_for = models.ForeignKey('self', on_delete=models.SET_NULL,
                                        blank=True, null=True,
                                        related_name='translations')

    format = models.CharField(max_length=50, blank=True)
    tags = ClusterTaggableManager(through=StoryTag, blank=True)

    author_ids = JSONField(default=list)
    type = models.ForeignKey(StoryType, on_delete=models.SET_NULL, blank=True,
                             null=True)
    template = models.ForeignKey(StoryTemplate, on_delete=models.PROTECT)
    dossier = models.ForeignKey(StoryDossier, on_delete=models.SET_NULL,
                                blank=True, null=True)
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

    @property
    def authors(self):
        rv = []
        for pk in self.author_ids:
            try:
                author = Author.objects.get(pk=pk)
            except Author.DoesNotExist:
                continue
            else:
                rv.append(author)
        return rv

    @property
    def stories_index(self):
        # Find closest ancestor which is a blog index
        return self.get_ancestors().type(StoriesIndex).last()

    @property
    def summary_or_intro(self):
        return self.summary or self.intro

    search_fields = Page.search_fields + [
        index.SearchField('summary'),
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('authors'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('summary', classname='full'),
        FieldPanel('intro', classname='full'),
        ImageChooserPanel('image'),
        MultiFieldPanel([
            FieldPanel('author_ids', widget=AuthorsWidget),
            FieldPanel('type'),
            FieldPanel('dossier'),
            FieldPanel('first_published_at'),
        ]),
        InlinePanel('locations', label="Locations"),
    ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel('tags'),
            ImageChooserPanel('feed_image'),
            FieldPanel('skip_home'),
        ], heading="Extra"),
        MultiFieldPanel([
            InlinePanel('related_pages', label="Related Pages"),
            InlinePanel('related_links', label="External links"),
        ], heading="Related"),
    ]

    blocks_panels = [
        StreamFieldPanel('body', classname='full'),
    ]

    settings_panels = Page.settings_panels + [
        PageChooserPanel('translation_for'),
        FieldPanel('template'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content details'),
        ObjectList(blocks_panels, heading='Content'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(settings_panels, heading='Settings', classname="settings"),
    ])

    def serve(self, request):
        template = f'blacktail/story/{self.template}.html'
        return render(request, template, {
            'page': self,
        })


class StoriesFolder(Page):
    date = models.DateField("Post date")
    summary = models.CharField(max_length=1000, blank=True)
    intro = models.CharField(max_length=1000, blank=True)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=StoriesFolderTag, blank=True)
    template = models.ForeignKey(StoriesFolderTemplate,
                                 on_delete=models.PROTECT)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='stories_folder_related'
    )
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    hide_title = models.BooleanField(default=False)

    search_fields = Page.search_fields + [
        index.SearchField('summary'),
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('summary', classname='full'),
        FieldPanel('intro', classname='full'),
        ImageChooserPanel('image'),
        FieldPanel('date'),
        FieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('feed_image'),
        FieldPanel('tags'),
    ]

    settings_panels = Page.settings_panels + [
        MultiFieldPanel([
            FieldPanel('template'),
            FieldPanel('hide_title'),
        ], heading="layout"),
    ]

    @property
    def summary_or_intro(self):
        return self.summary or self.intro

    def serve(self, request):
        template = f'blacktail/storiesfolder/{self.template}.html'
        stories = self.get_children().live().order_by('-first_published_at')

        return render(request, template, {
            'page': self,
            'stories': stories,
        })

@hooks.register('insert_editor_js')
def editor_js():
    return '''
        <script>
        $(function() {
            $('select').on('select2:select', function (evt) {
              var element = evt.params.data.element;
              if (evt.target.id == 'id_author_ids') {
                  $(element).detach();
                  $(this).append(element);
                  $(this).trigger('change');
              }
            });
            $('#id_author_ids').select2();
        });
        </script>
    '''
