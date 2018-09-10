from __future__ import absolute_import, unicode_literals

from django.db import models
from django.http.response import Http404

from wagtail.core.url_routing import RouteResult
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from wagtail.search import index

from .author import Author


class AboutPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    def get_context(self, request):

        context = super(AboutPage, self).get_context(request)
        authors = Author.objects.all()
        context['authors'] = authors

        return context


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

        context['model'] = Author.objects.get(pk=author_id)

        return context

    def route(self, request, path_components):
        if path_components:
            # request is for an author
            author_id = path_components[0]

            # find a matching author or 404
            try:
                Author.objects.get(pk=author_id)
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
