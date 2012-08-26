#!/usr/bin/env python
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

from google.appengine.ext import db
from google.appengine.ext.remote_api import remote_api_stub

import models

APP_NAME = 's~ffcapp'
os.environ['AUTH_DOMAIN'] = 'gmail.com'
os.environ['USER_EMAIL'] = 'adamjmcgrath@gmail.com'



def auth_func():
 return (os.environ['USER_EMAIL'], getpass.getpass('Password:'))


def main():
  # Use local dev server by passing in as parameter:
  # servername='localhost:8080'
  # Otherwise, remote_api assumes you are targeting APP_NAME.appspot.com
  remote_api_stub.ConfigureRemoteDatastore(APP_NAME, '/_ah/remote_api',
      auth_func, servername='ffcapp.appspot.com')

  cursor = None
  while True:
    logging.info('Updating a batch.')
    query = models.Film.all()
    if cursor:
      query.with_cursor(cursor)

    films = query.fetch(limit=1000)
    if not films:
      break

    for film in films:
      film.batch = 1
      film.grossing = None
      film.title_slug = models.slugify(film.title)

    db.put(films)
    cursor = query.cursor()


if __name__ == '__main__':
  main()
