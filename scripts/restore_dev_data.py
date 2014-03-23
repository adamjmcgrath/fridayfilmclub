#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Restore film data from app backup to dev server

To get entities from prod backup:

1. gsutil cp gs://ffcapp/backups/YYYYMMDD/** data/backups/YYYYMMDD/.
2. Run restore_dev_data.py
"""

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

from google.appengine.ext import ndb
from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.api.files import records
from google.appengine.datastore import entity_pb


import models

APP_NAME = 'dev~ffcapp'
os.environ['AUTH_DOMAIN'] = 'gmail.com'
os.environ['USER_EMAIL'] = 'adamjmcgrath@gmail.com'


def auth_func():
  return (os.environ['USER_EMAIL'], '')


def fix_emails():
  # TODO: Batch the datastore writes.
  print 'Fixing emails'
  for u in models.User.query():
    u.email = 'adamjmcgrath+%s@gmail.com' % u.username
    print u.email
    u.put()
  print 'Fixed emails'


def main():
  # Use 'localhost:8080' for dev server.
  remote_api_stub.ConfigureRemoteDatastore(APP_NAME, '/_ah/remote_api',
      auth_func, servername='localhost:8080')

  year = sys.argv[1]
  base_dir = 'data/backups/%s' % year

  for backup_file in os.listdir(base_dir):
    raw = open('%s/%s' % (base_dir, backup_file), 'r')
    reader = records.RecordsReader(raw)
    entities = []
    for record in reader:
      try:
        entity_proto = entity_pb.EntityProto(contents=record)
      except:
        break

      entity_proto.key().set_app(APP_NAME)
      for p in entity_proto.property_list():
        p.value().referencevalue().set_app(APP_NAME)

      entities.append(ndb.Model._from_pb(entity_proto))

    if len(entities):
      ndb.put_multi(entities)
      print 'restored: %s' % backup_file
  fix_emails()

if __name__ == '__main__':
  main()
