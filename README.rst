SpaceTrackApi client
____________________

Small helper for https://space-track.org query api.


Requirements
------------

- requests >= 2.14.2


Installing
__________

::

    pip install space-track-api


Getting started
---------------

To retrieve something from Space-Track:

.. code-block:: python

  # -*- coding: utf-8 -*-
  from __future__ import unicode_literals

  from pprint import pprint

  from space_track_api import SpaceTrackApi


  def main():
      with SpaceTrackApi(login='<YOUR_LOGIN>', password='<YOUR_PASSWORD>') as api:
          tle_list = api.tle(EPOCH='>now-3',
                             NORAD_CAT_ID=(25544, 25541,),
                             order_by=('EPOCH desc', 'NORAD_CAT_ID',),
                             predicate=('EPOCH', 'NORAD_CAT_ID', 'TLE_LINE0', 'TLE_LINE1', 'TLE_LINE2',))
          pprint(tle_list, indent=2)


  if __name__ == '__main__':
      main()


Source code
-----------

The latest developer version is available in a github repository:
https://github.com/nkoshell/space-track-api
