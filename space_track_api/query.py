# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections
import sys

from .exc import SpaceTrackEntityNotSupported

if sys.version_info >= (3, 0, 0):
    basestring = str
    unicode = str


SUPPORTABLE_ENTITIES = (
    'tle_latest',
    'tle_publish',
    'omm',
    'boxscore',
    'satcat',
    'launch_site',
    'satcat_change',
    'satcat_debut',
    'decay',
    'tip',
    'tle',
)


class SpaceTrackQueryBuilder(object):
    __slots__ = (
        '_filters',
        '_entity',
        '_order_by',
        '_limit',
        '_format',
        '_metadata',
        '_distinct',
        '_predicate',
    )

    def __init__(self, entity=None, order_by=None, limit=None,
                 fmt=None, metadata=False, distinct=True, predicate=None,
                 *args, **filters):

        self.entity = entity
        self.filters = filters
        self.predicate = predicate
        self.order_by = order_by
        self.limit = limit
        self.format = fmt
        self.metadata = metadata
        self.distinct = distinct

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, value):
        if isinstance(value, collections.Iterable) and not isinstance(value, basestring):
            value = tuple(value)
            value = value and value[0]

        if value is None:
            value = 'tle'

        if not isinstance(value, basestring):
            raise TypeError('Attribute `entity` must be basestring')
        elif value not in SUPPORTABLE_ENTITIES:
            raise SpaceTrackEntityNotSupported(self.entity)

        self._entity = value

    @property
    def order_by(self):
        return self._order_by

    @order_by.setter
    def order_by(self, value):
        if value is None:
            value = tuple()

        if isinstance(value, collections.Iterable) and not isinstance(value, basestring):
            value = tuple(value)

        if not isinstance(value, (basestring, collections.Iterable)):
            raise TypeError('Attribute `order_by` must be basestring or collections.Iterable')

        self._order_by = value

    @property
    def predicate(self):
        return self._predicate

    @predicate.setter
    def predicate(self, value):
        if value is None:
            value = tuple()

        if isinstance(value, collections.Iterable) and not isinstance(value, basestring):
            value = tuple(value)

        if not isinstance(value, (basestring, collections.Iterable)):
            raise TypeError('Attribute `predicate` must be basestring or collections.Iterable')

        self._predicate = value

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value):
        if isinstance(value, collections.Iterable) and not isinstance(value, basestring):
            value = tuple(value)
            value = value and value[0]

        if value is not None:
            value = int(value)

        self._limit = value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        if isinstance(value, collections.Iterable) and not isinstance(value, basestring):
            value = tuple(value)
            value = value and value[0]

        if value is None:
            value = 'json'

        if not isinstance(value, basestring):
            raise TypeError('Attribute `format` must be basestring')

        self._format = value

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        if isinstance(value, collections.Iterable) and not isinstance(value, basestring):
            value = tuple(value)
            value = value and value[0]

        self._metadata = bool(value)

    @property
    def distinct(self):
        return self._distinct

    @distinct.setter
    def distinct(self, value):
        if isinstance(value, collections.Iterable) and not isinstance(value, basestring):
            value = tuple(value)
            value = value and value[0]

        self._distinct = bool(value)

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, dictionary):
        _filters = collections.defaultdict(list)

        if isinstance(dictionary, dict):
            for key, value in dictionary.items():
                if isinstance(value, collections.Iterable) and not isinstance(value, (basestring, bytes)):
                    _filters[key].extend(value)
                else:
                    _filters[key].append(value)

        self._filters = _filters

    @property
    def query_params(self):
        return dict(entity=self.entity,
                    filters=self.serialize_multivalue(self.filters),
                    format=self.format,
                    limit=self.limit,
                    metadata="true" if self.metadata else "false",
                    order_by=self.serialize_multivalue(self.order_by),
                    predicates=self.serialize_multivalue(self.predicate))

    def query(self):
        q = ('basicspacedata/query/'
             'class/{entity}/'
             '{filters}/'
             'format/{format}/'
             'metadata/{metadata}/')

        if self.order_by:
            q += 'orderby/{order_by}/'

        if self.predicate:
            q += 'predicates/{predicates}/'

        if self.limit:
            q += 'limit/{limit}/'

        return q.format(**self.query_params)

    @staticmethod
    def serialize_multivalue(multivalue):
        if isinstance(multivalue, dict):
            return "/".join('{}/{}'.format(key, ",".join(unicode(value) for value in values))
                            for key, values in multivalue.items())
        elif isinstance(multivalue, collections.Iterable) and not isinstance(multivalue, basestring):
            return ",".join(unicode(value) for value in multivalue)

        return multivalue

    def __repr__(self):
        return '<{}("{}")>'.format(self.__class__.__name__, unicode(self))

    def __str__(self):
        return self()

    def __call__(self):
        return self.query()
