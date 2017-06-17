# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import contextlib
import io
import json
import logging
import os
from threading import Lock

from global_stopwords import settings
from global_stopwords.errors import GlobalStopwordsError

try:  # Python 2 # pragma: no cover
    from urllib2 import urlopen, Request, URLError

    str_types = (unicode, str)  # noqa
    text = unicode  # noqa
except ImportError:  # Python 3 # pragma: no cover
    from urllib.request import urlopen, Request
    from urllib.error import URLError

    str_types = (str,)
    text = str

# gevent monkey patched environment
try:  # pragma: no cover
    import socket
    import gevent.socket

    if socket.socket is gevent.socket.socket:
        from gevent import sleep
    else:
        from time import sleep
except (ImportError, AttributeError):  # pragma: no cover
    from time import sleep


logger = logging.getLogger(__package__)


class GlobalStopwords(object):
    def __init__(self, update=False):
        self.lock = Lock()

        self._data = self.load(update=update)

    def load(self, update=False):
        if update is False:
            if os.path.isfile(settings.CACHE_FILE):
                with io.open(
                    settings.CACHE_FILE, encoding='utf-8', mode='rt',
                ) as fp:
                    return json.loads(fp.read())

        attempts = 0

        url = settings.STOPWORDS_URL

        while True:
            attempts += 1

            request = Request(url)

            try:
                with contextlib.closing(
                    urlopen(
                        request,
                        timeout=settings.HTTP_TIMEOUT,
                    ),
                ) as response:
                    data = json.loads(response.read())

                    try:
                        with io.open(
                            settings.CACHE_FILE, encoding='utf-8', mode='wt',
                        ) as fp:
                            dumped = json.dumps(data)

                            if not isinstance(dumped, text):  # Python 2
                                dumped = dumped.decode('utf-8')

                            fp.write(dumped)
                    except IOError as exc:
                        msg = 'was unable to create cache file {file}'.format(
                            file=settings.CACHE_FILE,
                        )

                        logger.error(msg, exc_info=exc)

                    return data

            except (URLError, OSError) as exc:
                msg = 'Error occurred during fetching {url}'.format(
                    url=url,
                )

                logger.warning(msg, exc_info=exc)

                if attempts == settings.HTTP_RETRIES:
                    raise GlobalStopwordsError(
                        'Maximum amount of retries reached',
                    )
                else:
                    msg = 'Sleeping for {delay} seconds'.format(
                        delay=settings.HTTP_DELAY,
                    )

                    logger.debug(msg)

                    sleep(settings.HTTP_DELAY)

    def words(self, langs=None, silent=True):
        if langs:
            data = {}

            if isinstance(langs, str_types):
                langs = [langs]

            if not isinstance(langs, (tuple, list)):
                msg = 'langs should be passed as str, tuple or list'

                raise GlobalStopwordsError(msg)

            for lang in langs:
                if lang in self._data:
                    data.update({lang: self._data[lang]})
                else:
                    msg = 'stopwords for language {lang} were not found'.format(  # noqa
                        lang=lang,
                    )

                    if silent:
                        logger.warning(msg)
                    else:
                        raise GlobalStopwordsError(msg)

            return data or None
        else:
            return self._data
