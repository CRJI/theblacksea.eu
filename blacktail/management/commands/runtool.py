import sys
import os
import importlib
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

TOOLS = {
    name: importlib.import_module(f'blacktail.tools.{name}')
    for name in ['images_to_medium']
}


class Command(BaseCommand):

    help = 'Run a "fix content" tool'

    def add_arguments(self, parser):
        parser.add_argument('tool', choices=TOOLS.keys())
        parser.add_argument('-u', '--username', default=os.environ['USER'])
        parser.add_argument('-p', '--pk', type=int)

    def handle(self, tool, username, pk, *args, **options):
        user = User.objects.get(username=username)
        TOOLS[tool].handle(user, pk, out=sys.stdout)
