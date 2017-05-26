# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import re

import os
from setuptools import setup

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION_REGEXP = re.compile(r"^__version__ = [\'\"](.+?)[\'\"]$", re.MULTILINE)


def read(fn):
    with codecs.open(os.path.join(PROJECT_DIR, fn), encoding='utf-8') as f:
        return f.read().strip()


def version():
    try:
        return VERSION_REGEXP.findall(read(os.path.join('space_track_api', '__init__.py')))[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


vn = version()
url = 'https://github.com/nkoshell/space-track-api'

setup(
    name='space-track-api',
    description='Small helper for `space-track.org` query api.',
    long_description=read('README.rst'),
    version=vn,
    packages=['space_track_api'],
    url=url,
    download_url='{url}/archive/{version}.tar.gz'.format(url=url, version=vn),
    license='MIT',
    author='nkoshell',
    author_email='nikita.koshelev@gmail.com',
    install_requires=['requests>=2.14.2', 'ratelimiter>=1.1.1'],
)
