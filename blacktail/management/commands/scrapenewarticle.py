import uuid
import requests
from bs4 import BeautifulSoup
from slugify import slugify
import dateparser
import re
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from ...models import Story


class Command(BaseCommand):
    help = "Scrape a new article from the old website"

    def add_arguments(self, parser):
        parser.add_argument('target_url', nargs='+', type=str)

    def scrape_story(self, url):

        r = requests.get(url)
        bs = BeautifulSoup(r.text, 'html.parser')

        main_info = bs.find('div', 'main-info')
        content_sections = bs.find_all('section', re.compile("^content-"))
        content = ''

        for section in content_sections:
            content += section.prettify()

        try:
            footer = bs.find_all('footer')[0]
            content += footer.prettify()
        except:
            pass

        details = {
            'seo_title': bs.title.string,
            'title': main_info.h1.span.string,
            'intro': main_info.h2.span.string if main_info.h2 else main_info.h1.span.string,
            'authors': '1',
            'date': dateparser.parse(main_info.h4.span.string, languages=['en', 'tr', 'ro']),
            'content': content,
        }

        print("[{}] {}".format(
            details['date'],
            url
        ))

        return details

    def handle(self, *args, **options):
        urls = options['target_url']

        latest_story = Story.objects.all().order_by("-id")[0]
        next_id = latest_story.id + 1

        for url in urls:
            scraped = self.scrape_story(url)
            body = '[{"type": "aligned_html", "value": {"html": %s, "alignment": "normal"}, "id": "%s"}]'

            scraped['content'] = scraped['content'].replace('\\\\', '\\')

            try:
                story = Story()
                story.title = scraped['title']
                story.slug = slugify(scraped['title'])
                story.seo_title = scraped['title']
                story.date = scraped['date'].strftime('%Y-%m-%d')
                story.body = body % (str(scraped['content']), str(uuid.uuid4()))
                story.path = f'000100010002{next_id}'
                story.content_type = ContentType.objects.get_by_natural_key('blacktail', 'story')
                story.depth = 4

                story.save()

                Story.objects.filter(slug=slugify(scraped['title'])).update(id=next_id)
            except ValidationError:
                print(f"Slug already in use, skipping ({slugify(scraped['title'])})")
