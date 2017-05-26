# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pprint import pprint

from space_track_api import SpaceTrackApi, log


def main():
    with SpaceTrackApi(login='koshelev.n.a@yandex.ru', password='K0SHeLeV-941021') as api:
        tle_list = api.tle(EPOCH='>now-3',
                           NORAD_CAT_ID=(25544, 25541,),
                           order_by=('EPOCH desc', 'NORAD_CAT_ID',),
                           predicate=('EPOCH', 'NORAD_CAT_ID', 'TLE_LINE0', 'TLE_LINE1', 'TLE_LINE2',))
        pprint(tle_list, indent=2)


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG, format=log.DEFAULT_LOG_FORMAT)
    main()
