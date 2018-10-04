from django.core.management.base import BaseCommand
from ... import models


class Command(BaseCommand):
    #help = "Fixes html escapes in article titles"

    def handle(self, *args, **options):
        for story in models.Story.objects.order_by('first_published_at'):
            template = story.template.name if story.template else 'default'
            block_names = [i.block.name for i in story.body]
            print(f"{story.slug} (template:{template})", *block_names)
