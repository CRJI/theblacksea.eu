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
            if unescaped_title != page.title:
                print(f'Fixing html entities for {page.slug}')
                page.title = unescaped_title
                changed = True

            if "''" in page.title:
                print(f'Fixing double quotes for {page.slug}')
                page.title = page.title.replace("''", "'")
                changed = True

            if changed:
                page.save()
