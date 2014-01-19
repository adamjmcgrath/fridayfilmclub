#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Batch update film entities."""

import getpass
import logging
import os
import sys
import urllib2

APPENGINE_PATH = '/usr/local/google_appengine/'

def fix_appengine_path():
  EXTRA_PATHS = [
    APPENGINE_PATH,
    os.path.join(APPENGINE_PATH, 'lib', 'antlr3'),
    os.path.join(APPENGINE_PATH, 'lib', 'django'),
    os.path.join(APPENGINE_PATH, 'lib', 'fancy_urllib'),
    os.path.join(APPENGINE_PATH, 'lib', 'ipaddr'),
    os.path.join(APPENGINE_PATH, 'lib', 'webapp2'),
    os.path.join(APPENGINE_PATH, 'lib', 'webob-1.1.1'),
    os.path.join(APPENGINE_PATH, 'lib', 'yaml', 'lib'),
    os.path.join(APPENGINE_PATH, 'lib', 'webapp2-2.5.2'),
  ]
  sys.path.extend(EXTRA_PATHS)

fix_appengine_path()

# Add models to path.
sys.path.insert(0, '/Users/adammcgrath/dev/projects/ffc/src/')

from google.appengine.ext import ndb
from google.appengine.ext.remote_api import remote_api_stub

import models

APP_NAME = 's~ffcapp'
os.environ['AUTH_DOMAIN'] = 'gmail.com'
os.environ['USER_EMAIL'] = 'adamjmcgrath@gmail.com'

ANSWERS = [
  {
    'key': ndb.Key('Film', '1989-national-lampoons-christmas-vacation', app='s~ffcapp'),
    'id': '/en/national_lampoons_christmas_vacation'
  },
  {
    'key': ndb.Key('Film', '1992-the-bodyguard', app='s~ffcapp'),
    'id': '/en/the_bodyguard'
  },
  {
    'key': ndb.Key('Film', '1993-groundhog-day', app='s~ffcapp'),
    'id': '/en/groundhog_day_1993'
  },
  {
    'key': ndb.Key('Film', '1993-philadelphia', app='s~ffcapp'),
    'id': '/en/philadelphia_1993'
  },
  {
    'key': ndb.Key('Film', '1991-hook', app='s~ffcapp'),
    'id': '/en/hook'
  },
  {
    'key': ndb.Key('Film', '2010-kickass', app='s~ffcapp'),
    'id': '/wikipedia/ru_id/1717630'
  },
  {
    'key': ndb.Key('Film', '1983-national-lampoons-vacation', app='s~ffcapp'),
    'id': '/en/national_lampoons_european_vacation'
  },
  {
    'key': ndb.Key('Film', '2001-ai-artificial-intelligence', app='s~ffcapp'),
    'id': '/en/a_i'
  },
  {
    'key': ndb.Key('Film', '1987-the-lost-boys', app='s~ffcapp'),
    'id': '/en/the_lost_boys'
  },
  {
    'key': ndb.Key('Film', '2007-atonement', app='s~ffcapp'),
    'id': '/en/atonement_2007'
  },
  {
    'key': ndb.Key('Film', '1986-ferris-buellers-day-off', app='s~ffcapp'),
    'id': '/en/ferris_buellers_day_off'
  },
]


def auth_func():
  return (os.environ['USER_EMAIL'], getpass.getpass('Password:'))


def main():
  # Use 'localhost:8080' for dev server.
  remote_api_stub.ConfigureRemoteDatastore(APP_NAME, '/_ah/remote_api',
      auth_func, servername='ffcapp.appspot.com')

  for a in ANSWERS:
    print models.Question.query(models.Question.answer == a['key']).get()
    f = urllib2.urlopen('http://films-data.appspot.com/api?id=' + a['id'])
    print f.read()


if __name__ == '__main__':
  main()
