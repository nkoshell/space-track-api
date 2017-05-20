# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from requests import Session
from .query import SpaceTrackQueryBuilder


class SpaceTrackApi(object):
    def __init__(self, login, password, session=None, **kwargs):
        self.logger = kwargs.pop('logger', logging.getLogger('{}.{}'.format(__name__, self.__class__.__name__)))
        self.credentials = dict(identity=login, password=password)
        self.session = session if isinstance(session, Session) else Session()
        self.url = kwargs.pop('url', 'https://www.space-track.org')
        self.query_url = kwargs.pop('query_url', 'basicspacedata/query')
        self.login_url = kwargs.pop('login_url', 'ajaxauth/login')
        self.logout_url = kwargs.pop('logout_url', 'ajaxauth/logout')

    def tle_latest(self, **kwargs):
        kwargs['entity'] = 'tle_latest'
        return self.query(**kwargs)

    def tle_publish(self, **kwargs):
        kwargs['entity'] = 'tle_publish'
        return self.query(**kwargs)

    def omm(self, **kwargs):
        kwargs['entity'] = 'omm'
        return self.query(**kwargs)

    def boxscore(self, **kwargs):
        kwargs['entity'] = 'boxscore'
        return self.query(**kwargs)

    def satcat(self, **kwargs):
        kwargs['entity'] = 'satcat'
        return self.query(**kwargs)

    def launch_site(self, **kwargs):
        kwargs['entity'] = 'launch_site'
        return self.query(**kwargs)

    def satcat_change(self, **kwargs):
        kwargs['entity'] = 'satcat_change'
        return self.query(**kwargs)

    def satcat_debut(self, **kwargs):
        kwargs['entity'] = 'satcat_debut'
        return self.query(**kwargs)

    def decay(self, **kwargs):
        kwargs['entity'] = 'decay'
        return self.query(**kwargs)

    def tip(self, **kwargs):
        kwargs['entity'] = 'tip'
        return self.query(**kwargs)

    def tle(self, **kwargs):
        return self.query(**kwargs)

    def query(self, **kwargs):
        qb = SpaceTrackQueryBuilder(**kwargs)
        url = '{url}/{query}'.format(url=self.url, query=qb)
        self.logger.info('Send request to %s', url)
        resp = self.session.get(url)
        try:
            m = getattr(resp, self.get_response_method(qb.format))
            return m() if callable(m) else m
        except Exception as e:
            self.logger.exception(e)
            return resp.text

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

    def login(self):
        resp = self.session.post('{}/{}'.format(self.url, self.login_url), data=self.credentials)
        if resp.reason == 'OK':
            self.logger.info('"Successfully logged in"')
            return self.session

    def logout(self):
        resp = self.session.get('{}/{}'.format(self.url, self.logout_url))
        if resp.reason == 'OK':
            self.logger.info(resp.text)

    def close(self):
        self.session.close()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, *args):
        self.logout()
        self.close()
