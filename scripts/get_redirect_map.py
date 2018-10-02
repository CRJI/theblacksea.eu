#!/usr/bin/env python

import re
from io import StringIO
import csv
from pathlib import Path
import json
import requests

STORIES_MAP = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQAOgWzHGdtel374RTvjB8iazqSFYXjh6VhlVR8XlV5BL7tlxvzc_70FemaAPkplCgoQFqADxMkJru2/pub?gid=1480092930&single=true&output=csv'
BLOGS_MAP = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQAOgWzHGdtel374RTvjB8iazqSFYXjh6VhlVR8XlV5BL7tlxvzc_70FemaAPkplCgoQFqADxMkJru2/pub?gid=50424262&single=true&output=csv'


def load_sheet(url):
    return [
        (r['old'], r['new'])
        for r in csv.DictReader(StringIO(requests.get(url).text))
    ]


def strip(url):
    return re.sub(r'^http[s]?://[^/]+', '', url)


def main():
    redirect = {
            strip(old): strip(new)
            for old, new in
            load_sheet(STORIES_MAP) + load_sheet(BLOGS_MAP)
            if new
        }
    path = Path(__file__).parent.parent / 'redirect.json'
    with path.open('w', encoding='utf8') as f:
        print(json.dumps(redirect, indent=2, sort_keys=True), file=f)


main()
