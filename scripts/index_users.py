#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Reindex all users in the datastore."""

import getpass
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
    os.path.join(APPENGINE_PATH, 'lib', 'webob-1.1.1'),
    os.path.join(APPENGINE_PATH, 'lib', 'yaml', 'lib'),
    os.path.join(APPENGINE_PATH, 'lib', 'webapp2-2.5.2'),
  ]
  sys.path.extend(EXTRA_PATHS)

fix_appengine_path()

# Add models to path.
sys.path.insert(0, '/Users/adammcgrath/dev/projects/ffc/src/')

from google.appengine.ext.remote_api import remote_api_stub


import models
import usersearch

APP_NAME = 'dev~ffcapp'
BATCH_SIZE = 50
os.environ['AUTH_DOMAIN'] = 'gmail.com'
os.environ['USER_EMAIL'] = 'adamjmcgrath@gmail.com'


def auth_func():
  return os.environ['USER_EMAIL'], getpass.getpass('Password:')


def index_users(curs=None):
  print 'Indexing %d users' % BATCH_SIZE
  users, next_curs, more = models.User.query().fetch_page(BATCH_SIZE,
                                                          start_cursor=curs)
  usersearch.index_users(users)

  if more:
    index_users(next_curs)


def main():
  # Use 'servername='ffcapp.appspot.com' for prod.
  remote_api_stub.ConfigureRemoteDatastore(APP_NAME, '/_ah/remote_api',
      auth_func, servername='localhost:8080')

  index_users()


if __name__ == '__main__':
  main()
