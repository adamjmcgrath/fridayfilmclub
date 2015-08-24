#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Migrate images from blobstore to cloud storage

You'll need to `pip install python-magic`
"""

import os
import sys
sys.path.append('/usr/local/google_appengine')
import dev_appserver
import posixpath
import cloudstorage
import magic
import re
import getpass

dev_appserver.fix_sys_path()

dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(dir, '../src'))

from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.ext import blobstore, ndb

GCS_ROOT = '/ffcapp.appspot.com/images/'

os.environ['SERVER_SOFTWARE'] = 'Development (remote_api)/1.0'

import models

APP_NAME = 's~ffcapp'
RE_SPECIAL_CHARS_ = re.compile(r'[^a-zA-Z0-9 ]')
os.environ['AUTH_DOMAIN'] = 'gmail.com'
os.environ['USER_EMAIL'] = 'adamjmcgrath@gmail.com'

def slugify(my_string):
  """Remove special characters and replace spaces with hyphens."""
  return '-'.join(re.sub(RE_SPECIAL_CHARS_, '', my_string).lower().split(' '))

def auth_func():
  return (os.environ['USER_EMAIL'], getpass.getpass())

def save_image(blob_key, folder_name, file_name):
  if not blob_key:
    print 'ERROR: no blob %s/%s' % (folder_name, file_name)
    return blob_key

  img_file = blobstore.BlobInfo(blob_key)
  img_file_o = img_file.open()
  img_data = img_file_o.read()
  type = magic.from_buffer(img_data, mime=True)

  file_path = posixpath.join(
    GCS_ROOT, folder_name, file_name)
  gcs_file = cloudstorage.open(file_path, 'w', content_type=type)
  print 'Saving file: %s' % file_path
  gcs_file.write(img_data)
  gcs_file.close()
  img_file_o.close()
  return blobstore.BlobKey(blobstore.create_gs_key('/gs' + file_path))


def migrate_screenshot(q):
  clue = q.clues[0]
  if not clue:
    return
  title = q.answer_title
  clue_entity = clue.get()
  old_key = str(clue_entity.image)
  clue_entity.image = save_image(
    clue_entity.image, 'questions', slugify(title) + '-screenshot')
  clue_entity.put()
  print ('screenshot: %s | old: %s | new: %s' % (title, old_key, str(clue_entity.image)))


def migrate_packshot(q):
  title = q.answer_title
  old_key = str(q.packshot)
  q.packshot = save_image(
    q.packshot, 'questions', slugify(title) + '-packshot')
  q.put()
  print ('packshot: %s | old: %s | new: %s' % (title, old_key, str(q.packshot)))


def migrate_questions():
  for q in models.Question.query():
    migrate_packshot(q)
    migrate_screenshot(q)

def migrate_users(curs=None):
  users, next_curs, more = models.User.query().fetch_page(500,
                                                          start_cursor=curs)
  for u in users:
    old_key = str(u.pic)
    u.pic = save_image(u.pic, 'profiles', u.username_lower)
    print ('profile: %s | old: %s | new: %s' % (u.username_lower, old_key, str(u.pic)))

  ndb.put_multi(users)

  if more:
    migrate_users(next_curs)


def migrate_leagues(curs=None):
  leagues, next_curs, more = models.League.query().fetch_page(500,
                                                              start_cursor=curs)

  for l in leagues:
    old_key = str(l.pic)
    l.pic = save_image(l.pic, 'leagues', l.name_slug)
    print ('league: %s | old: %s | new: %s' % (l.name_slug, old_key, str(l.pic)))

  ndb.put_multi(leagues)

  if more:
    migrate_leagues(next_curs)


def main():
  # Use 'localhost:8080' for dev server.
  remote_api_stub.ConfigureRemoteApi(APP_NAME, '/_ah/remote_api',
      auth_func, servername='ffcapp.appspot.com')

  migrate_questions()
  migrate_users()
  migrate_leagues()


if __name__ == '__main__':
  main()
