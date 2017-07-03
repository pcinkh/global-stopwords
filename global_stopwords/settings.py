# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import tempfile

__version__ = '0.0.1'

CACHE_FILE = os.path.join(
    tempfile.gettempdir(),
    'global_stopwords_{version}.json'.format(version=__version__),
)

STOPWORDS_VERSION = 'v1.2.0'

STOPWORDS_URL = 'https://raw.githubusercontent.com/6/stopwords-json/{stopwords_version}/stopwords-all.json'.format(  # noqa
    stopwords_version=STOPWORDS_VERSION,
)

HTTP_DELAY = 5

HTTP_TIMEOUT = 10

HTTP_RETRIES = 3
