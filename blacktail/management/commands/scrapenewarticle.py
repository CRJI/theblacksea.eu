import uuid
import requests
from bs4 import BeautifulSoup
from slugify import slugify
import dateparser
import re
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from wagtail.core.models import Page
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

        def get_next_id(model_class):
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute( "select nextval('%s_id_seq')" % model_class._meta.db_table)
            row = cursor.fetchone()
            cursor.close()
            return row[0]

        for url in urls:
            print()
            scraped = self.scrape_story(url)

            body = '[{"type": "aligned_html", "value": {"html": %s, "alignment": "normal"}, "id": "%s"}]'
            scraped['content'] = scraped['content'].replace('\\\\', '\\')

            details = {
                'title': scraped['title'],
                'body': body % (str(scraped['content']), str(uuid.uuid4())),
                'slug': slugify(scraped['title']),
                'date': scraped['date'].strftime('%Y-%m-%d'),
                'depth': 4,
                'seo_title': scraped['title'],
                'content_type': ContentType.objects.get_by_natural_key('blacktail', 'story'),
            }

            try:
                story = Story.objects.get(slug = slugify(scraped['title']))
                for key in ['title', 'seo_title', 'slug', 'date', 'body']:
                    setattr(story, key, details[key])
                story.save()
                print(f"Updated: {story.id} / {story.slug}")
            except Story.DoesNotExist:
                story = Story()

                next_id = get_next_id(Page) + 1         # this is not thread safe, if anyone cares
                story.path = f'000100010002{next_id}'

                for key, value in details.items():
                    setattr(story, key, value)
                story.save()
                print(f"Created: {next_id} / {slugify(scraped['title'])}")
            except ValidationError as e:
                print(f"Validation error, skipping ({slugify(scraped['title'])})")
                print(f"{e}")
            print()
