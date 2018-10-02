#!/usr/bin/env python

from io import StringIO
import re
import csv
import sys
import requests

GIST = 'https://gist.githubusercontent.com/mgax/65295573844f6daaf611e38989937397'
WAGTAIL = 'https://wagtail.theblacksea.eu'
LOCAL = 'http://theblacksea.carbon'
OLDSITE = 'https://theblacksea.eu'

CURRENT_MAP = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQAOgWzHGdtel374RTvjB8iazqSFYXjh6VhlVR8XlV5BL7tlxvzc_70FemaAPkplCgoQFqADxMkJru2/pub?gid=1480092930&single=true&output=csv'
MANUAL_MAP = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQAOgWzHGdtel374RTvjB8iazqSFYXjh6VhlVR8XlV5BL7tlxvzc_70FemaAPkplCgoQFqADxMkJru2/pub?gid=1590954652&single=true&output=csv'

def normalize(url):
    return re.sub(r'^(http[s]?://(www\.)?theblacksea.eu)?(/)?', '/', url)

def load_sheet(url):
    return [
        (r['old'], r['new'])
        for r in csv.DictReader(StringIO(requests.get(url).text))
    ]

def map_urls():
    current_map = load_sheet(CURRENT_MAP)
    manual_map = dict(load_sheet(MANUAL_MAP))
    # old_story_urls = requests.get(f'{GIST}/raw/stories.json').json()
    for old, new in current_map:
        if not new:
            new = manual_map.get(old, '')
        #url = normalize(url)
        #resp = requests.get(f'{LOCAL}{url}')
        #ok = '<div class="container-fluid">' in resp.text
        #old = f'{OLDSITE}{url}'
        #new = resp.url.replace(LOCAL, WAGTAIL) if ok else ''
        yield old, new

def main():
    writer = csv.writer(sys.stdout, delimiter='\t')
    writer.writerow(['old', 'new'])
    for old, new in map_urls():
        writer.writerow([old, new])

main()
