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


class Location(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
    ]

    class Meta:
        abstract = True

class StoryLocation(Orderable, Location):
    page = ParentalKey('blacktail.Story', related_name='locations')

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

class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"

class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'), ('mid', 'Mid width'), ('full', 'Full width'),
    ))

class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))

class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()

class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"

class BlogStreamBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    aligned_image = ImageBlock(label="Aligned image", icon="image")
    pullquote = PullQuoteBlock()
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    document = DocumentChooserBlock(icon="doc-full-inverse")

class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    api_fields = ['link_external', 'link_page', 'link_document']

    class Meta:
        abstract = True

class ContactFields(models.Model):
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=10, blank=True)

    panels = [
        FieldPanel('telephone'),
        FieldPanel('email'),
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('post_code'),
    ]

    api_fields = ['telephone', 'email', 'address_1', 'address_2', 'city', 'country', 'post_code']

    class Meta:
        abstract = True


# Related links
class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    api_fields = ['title'] + LinkFields.api_fields

    class Meta:
        abstract = True

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

class BlogPost(Page):
    date = models.DateField("Post date")
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    # tags = ClusterTaggableManager(through=StoryTag, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('date'),
        FieldPanel('intro', classname='full'),
        FieldPanel('body', classname='full'),
    ]

class Story(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=255, blank=True)
    body_richtext = RichTextField(blank=True)
    body_blocks = StreamField(BlogStreamBlock(), blank=True)
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
        index.SearchField('body_richtext'),
        index.SearchField('body_blocks'),
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

    text_panels = [
        FieldPanel('body_richtext', classname='full'),
    ]

    blocks_panels = [
        StreamFieldPanel('body_blocks', classname='full'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content details'),
        ObjectList(text_panels, heading='Text'),
        ObjectList(blocks_panels, heading='Blocks'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

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
        blog_list = BlogPost.objects.live()
        story_list = Story.objects.live()
        context['all_posts'] = sorted(
            chain(blog_list, story_list),
            key=attrgetter('date'))
        return context

class StaticPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full')
    ]
