from __future__ import absolute_import, unicode_literals

import dj_database_url

from .base import *

DEBUG = False

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://postgres:secret@127.0.0.1:5432/tbs'
    )
}

try:
    from .local import *
except ImportError:
    pass
