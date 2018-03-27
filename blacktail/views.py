from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.core.models import Page
from wagtail.search.models import Query

from . import models


def search(request):
    # Search
    search_query = request.GET.get('query', None)
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()

        # Get search picks
        search_picks = query.editors_picks.all()
    else:
        search_results = Page.objects.none()

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'blacktail/search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
        'search_picks': search_picks,
    })


def index_php(request):
    pk = request.GET.get('idRec')
    story = models.Story.objects.filter(pk=pk).first()
    blog_post = models.BlogPost.objects.filter(pk=pk).first()
    page = story or blog_post
    url = None
    if page:
        url = page.get_url(request)
        return HttpResponseRedirect(url)

    raise Http404
