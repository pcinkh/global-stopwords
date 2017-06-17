# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import tempfile

__version__ = '0.0.1'

CACHE_FILE = os.path.join(
    tempfile.gettempdir(),
    'global_stopwords.json',
)

STOPWORDS_URL = 'https://raw.githubusercontent.com/6/stopwords-json/master/stopwords-all.json'  # noqa

HTTP_DELAY = 5

HTTP_TIMEOUT = 10

HTTP_RETRIES = 3
