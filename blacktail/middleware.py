from pathlib import Path
import json
import re
from django.http import HttpResponseRedirect

URLMAP_PATH = Path(__file__).parent.parent / 'redirect.json'

def redirect(get_response):

    with Path(URLMAP_PATH).open(encoding='utf8') as f:
        urlmap = json.load(f)

    def middleware(request):
        raw_uri = request.get_raw_uri()
        path = re.sub(r'^http[s]?://[^/]+', '', raw_uri).rstrip('/')
        url = urlmap.get(path) or urlmap.get(path + '/')
        if url:
            return HttpResponseRedirect(url)

        return get_response(request)

    return middleware
