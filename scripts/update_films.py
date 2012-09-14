#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Batch update film entities."""

import getpass
import logging
import os
import sys

APPENGINE_PATH = '/usr/local/google_appengine/'

def fix_appengine_path():
  EXTRA_PATHS = [
    APPENGINE_PATH,
    os.path.join(APPENGINE_PATH, 'lib', 'antlr3'),
    os.path.join(APPENGINE_PATH, 'lib', 'django'),
    os.path.join(APPENGINE_PATH, 'lib', 'fancy_urllib'),
    os.path.join(APPENGINE_PATH, 'lib', 'ipaddr'),
    os.path.join(APPENGINE_PATH, 'lib', 'webapp2'),
    os.path.join(APPENGINE_PATH, 'lib', 'webob_1_1_1'),
    os.path.join(APPENGINE_PATH, 'lib', 'yaml', 'lib'),
  ]
  sys.path.extend(EXTRA_PATHS)

fix_appengine_path()

# Add models to path.
sys.path.insert(0, '/Users/adam/dev/projects/ffc/src/')

from google.appengine.ext import ndb
from google.appengine.ext.remote_api import remote_api_stub

import models

APP_NAME = 's~ffcapp'
os.environ['AUTH_DOMAIN'] = 'gmail.com'
os.environ['USER_EMAIL'] = 'adamjmcgrath@gmail.com'



def auth_func():
  return (os.environ['USER_EMAIL'], getpass.getpass('Password:'))


def main():
  # Use 'localhost:8080' for dev server.
  remote_api_stub.ConfigureRemoteDatastore(APP_NAME, '/_ah/remote_api',
      auth_func, servername='ffcapp.appspot.com')

  cursor = None
  while True:
    print 'Updating a batch.'
    query = models.Film.query()
    if cursor:
      query.with_cursor(cursor)
  
    films = query.fetch(limit=1000)
    if not films:
      break
  
    for film in films:
      film.title_slug = models.slugify(film.title)
      print film.title + ': ' + film.title_slug
  
    ndb.put_multi(films)
    cursor = query.cursor()


if __name__ == '__main__':
  main()
