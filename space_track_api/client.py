# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

import logging
from contextlib import closing
from functools import partial

from ratelimiter import RateLimiter
from requests import Session

from .query import SpaceTrackQueryBuilder, SUPPORTABLE_ENTITIES


class SpaceTrackApi(object):
    def __init__(self, login, password, session=None, **kwargs):
        self.logger = kwargs.pop('logger', logging.getLogger('{}.{}'.format(__name__, self.__class__.__name__)))
        self.credentials = dict(identity=login, password=password)
        self.session = session if isinstance(session, Session) else Session()
        self.url = kwargs.pop('url', 'https://www.space-track.org')
        self.query_url = kwargs.pop('query_url', 'basicspacedata/query')
        self.login_url = kwargs.pop('login_url', 'ajaxauth/login')
        self.logout_url = kwargs.pop('logout_url', 'ajaxauth/logout')

    @RateLimiter(max_calls=20, period=60)
    def query(self, **kwargs):
        qb = SpaceTrackQueryBuilder(**kwargs)
        url = '{url}/{query}'.format(url=self.url, query=qb)
        self.logger.info('Send request to %s', url)
        with closing(self.session.get(url)) as resp:
            try:
                m = getattr(resp, self.get_response_method(qb.format))
                return m() if callable(m) else m
            except Exception as e:
                self.logger.exception(e)
                return resp.text

    def login(self):
        with closing(self.session.post('{}/{}'.format(self.url, self.login_url), data=self.credentials)) as resp:
            if resp.reason == 'OK':
                self.logger.info('"Successfully logged in"')
                return self.session

    def logout(self):
        with closing(self.session.get('{}/{}'.format(self.url, self.logout_url))) as resp:
            if resp.reason == 'OK':
                self.logger.info(resp.text)

    def close(self):
        self.session.close()

    @staticmethod
    def get_response_method(fmt):
        method_mapping = {
            'json': 'json',
            'xml': 'text',
            'html': 'text',
            'csv': 'text',
            'tle': 'text',
            '3le': 'text',
            'kvn': 'text',
            'stream': 'iter_content'
        }
        return method_mapping.get(fmt, 'content')

    def __call__(self, **kwargs):
        return self.query(**kwargs)

    def __getattr__(self, item):
        if item not in SUPPORTABLE_ENTITIES:
            raise AttributeError('`{!r}` object has no attribute "{}"'.format(self, item))
        return partial(self.query, entity=item)

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, *args):
        self.logout()
        self.close()
