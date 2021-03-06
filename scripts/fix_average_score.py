#!/usr/bin/env python
# coding=utf-8
#
# Copyright Friday Film Club. All Rights Reserved.

"""Update average score so that archive questions aren't included."""

import os
import sys
import getpass
import datetime

APPENGINE_PATH = os.path.abspath(os.environ['APPENGINE_SRC'])
APPENGINE_DEV_APPSERVER =  os.path.join(APPENGINE_PATH, 'dev_appserver.py')
APPENGINE_APP_CFG =  os.path.join(APPENGINE_PATH, 'appcfg.py')

sys.path.append(APPENGINE_PATH)
import dev_appserver
dev_appserver.fix_sys_path()

from google.appengine.ext import ndb
from google.appengine.ext.remote_api import remote_api_stub

import models

APP_NAME = 's~ffcapp'
os.environ['AUTH_DOMAIN'] = 'gmail.com'
os.environ['USER_EMAIL'] = 'adamjmcgrath@gmail.com'


def auth_func():
  return os.environ['USER_EMAIL'], getpass.getpass('Password:')

def get_uqs(u):
  return [uq for uq in models.UserQuestion.query(
    models.UserQuestion.user==u.key,
    models.UserQuestion.complete==True,
   ndb.OR(models.UserQuestion.score==0, models.UserQuestion.score==None))]

def fix_user(u):
  uqs = get_uqs(u)
  lus = models.LeagueUser.query(models.LeagueUser.user==u.key)

  correction = 0

  for uq in uqs:
    if (uq.created and
       (uq.created - uq.question.get().posed) > datetime.timedelta(days=7)):
      correction += 1

  u.active_questions_answered = u.questions_answered - correction
  print '%s: old: %d, new: %d' % (u.username, u.questions_answered, u.active_questions_answered)
  if u.active_questions_answered > 0:
    u.put()

  for lu in lus:
    l_correction = 0
    league = lu.league.get()
    for uq in uqs:
      if (uq.created and
          uq.created.date() > league.created and
         (uq.created - uq.question.get().posed) > datetime.timedelta(days=7)):
        l_correction += 1
    lu.active_questions_answered = lu.questions_answered - l_correction
    print '  league - %s: old: %d, new: %d' % (u.username, lu.questions_answered, lu.active_questions_answered)
    if lu.active_questions_answered > 0:
      lu.put()


def main():
  # Use 'localhost:8080' for dev server.
  remote_api_stub.ConfigureRemoteDatastore(APP_NAME, '/_ah/remote_api',
      auth_func, servername='ffcapp.appspot.com')

  for u in models.User.query():
    fix_user(u)

if __name__ == '__main__':
  main()
