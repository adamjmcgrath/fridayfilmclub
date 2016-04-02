#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Restore film data from app backup to dev server

To get entities from prod backup:

1. gsutil -m cp gs://ffcapp.appspot.com/backups/YY-MM-DD data/backups/.
2. Run restore_dev_data.py YY-MM-DD
"""

import os
import sys
sys.path.append('/usr/local/google_appengine')
import dev_appserver

dev_appserver.fix_sys_path()

dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(dir, '../src'))

from google.appengine.ext import ndb
from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.api.files import records
from google.appengine.datastore import entity_pb


import models

APP_NAME = 'dev~ffcapp'
BATCH_SIZE = 100
os.environ['AUTH_DOMAIN'] = 'gmail.com'
os.environ['USER_EMAIL'] = 'adamjmcgrath@gmail.com'


def auth_func():
  return (os.environ['USER_EMAIL'], '')


def fix_emails(curs=None):
  print 'Fixing emails'
  users, next_curs, more = models.User.query().fetch_page(BATCH_SIZE,
                                                          start_cursor=curs)
  for u in users:
    u.email = 'adamjmcgrath+%s@gmail.com' % u.username
  ndb.put_multi(users)

  if more:
    fix_emails(next_curs)

def recursive_walk(folder):
  for folderName, subfolders, filenames in os.walk(folder):
    if subfolders:
      for subfolder in subfolders:
        recursive_walk(subfolder)
    print('\nFolder: ' + folderName + '\n')
    for filename in filenames:
      handle_file(folderName, filename)

def handle_file(base_dir, backup_file):
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

def main():
  remote_api_stub.ConfigureRemoteDatastore(APP_NAME, '/_ah/remote_api',
      auth_func, servername='localhost:8080')

  year = sys.argv[1]
  base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '../data/backups/%s' % year)

  recursive_walk(base_dir)

  fix_emails()

if __name__ == '__main__':
  main()
