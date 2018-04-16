from django.core.management.base import BaseCommand
from django.db import connection, IntegrityError
import os
import sys
import json

cursor = connection.cursor()

class Command(BaseCommand):
    help = "Imports all authors from the given Django pages fixture"

    def add_arguments(self, parser):
        parser.add_argument('fixture_path', type=str)
        parser.add_argument('page_type', type=str, help='Page type (blog / story)')

        parser.add_argument('-n', '--no-commit', dest='dry', action='store_true')
        parser.set_defaults(no_commit=False)

    def read_authors(self, raw_json):
        mapping = dict()
        for article in raw_json:
            pk = article['pk']
            authors = article['fields']['authors']
            mapping[pk] = authors
        return mapping

    def handle(self, *args, **options):
        fixture_path = options['fixture_path']
        page_type = options['page_type']
        dry = options['dry']

        if page_type == 'blog':
            table_name = 'blacktail_blogpost_authors'
            page_column = 'blogpost_id'
        else:
            table_name = 'blacktail_story_authors'
            page_column = 'story_id'

        with open(fixture_path, 'r') as fixture:
            mapping = self.read_authors(json.load(fixture))

            for pk, authors_list in mapping.items():
                for author_id in authors_list:
                    sql = f'INSERT INTO {table_name} ({page_column}, author_id) VALUES (%s, %s)'

                    if not dry:
                        print(sql % (pk, author_id))
                        try:
                            cursor.execute(sql, (pk, author_id))
                        except IntegrityError as e:
                            print('Skipping due to integrity error')
                    else:
                        print(sql % (pk, author_id))
