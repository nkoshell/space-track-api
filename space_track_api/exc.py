# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class SpaceTrackEntityNotSupported(Exception):
    def __init__(self, entity=None):
        super(SpaceTrackEntityNotSupported, self).__init__('Entity "%s" not supported' % entity)
