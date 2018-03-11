import html
from django.core.management.base import BaseCommand
from ... import models


class Command(BaseCommand):
    help = "Fixes html escapes in article titles"

    def handle(self, *args, **options):
        for story in models.Story.objects.all():
            changed = False

            unescaped_title = html.unescape(story.title)
            if unescaped_title != story.title:
                print(f'Fixing html entities for {story.slug}')
                story.title = unescaped_title
                changed = True

            if "''" in story.title:
                print(f'Fixing double quotes for {story.slug}')
                story.title = story.title.replace("''", "'")
                changed = True

            if changed:
                story.save()
