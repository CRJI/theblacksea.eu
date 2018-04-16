import html
from django.core.management.base import BaseCommand
from ... import models


class Command(BaseCommand):
    help = "Fixes html escapes in article titles"

    def handle(self, *args, **options):
        def iterpages():
            yield from models.Story.objects.all()
            yield from models.BlogPost.objects.all()

        for page in iterpages():
            changed = False

            unescaped_title = html.unescape(page.title)
            unescaped_seo_title = html.unescape(page.seo_title)

            if unescaped_title != page.title:
                print(f'Fixing html entities for {page.slug} (title)')
                page.title = unescaped_title
                changed = True

            if unescaped_seo_title != page.seo_title:
                print(f'Fixing html entities for {page.slug} (seo_title)')
                page.seo_title = unescaped_seo_title
                changed = True

            if "''" in page.title:
                print(f'Fixing double quotes for {page.slug} (title)')
                page.title = page.title.replace("''", "'")
                changed = True

            if "''" in page.seo_title:
                print(f'Fixing double quotes for {page.slug} (seo_title)')
                page.seo_title = page.seo_title.replace("''", "'")
                changed = True

            if "''" in page.intro:
                print(f'Fixing double quotes for {page.slug} (intro)')
                page.intro = page.intro.replace("''", "'")
                changed = True

            if changed:
                page.save()
