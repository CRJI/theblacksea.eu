from pathlib import Path
from django.core.management.base import BaseCommand
from wagtail.images.models import Rendition


class Command(BaseCommand):
    help = "Deletes the image rendition cache"

    def handle(self, *args, **options):
        for rendition in Rendition.objects.all():
            path = Path(rendition.file.path)
            if path.is_file():
                path.unlink()
            rendition.delete()
            print('.', end='', flush=True)
        print()
