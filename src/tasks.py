#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

"""Async tasks for Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import datetime
import logging

from google.appengine.api import taskqueue
from google.appengine.ext import deferred, blobstore, ndb
from webapp2_extras.appengine.auth.models import UserToken

import baserequesthandler
import models

BATCH_SIZE = 100
BACKUP_ENTITIES = [
  'Clue',
  'Question',
  'Season',
  'User',
  'UserQuestion',
  'UserSeason',
  'UserToken',
  'League',
  'LeagueUser',
]


def delete_user(user_id, anonymous=False):
  """Delete the User and associated pic, UserQuestions and UserSeasons."""

  cls = models.AnonymousUser if anonymous else models.User
  user = cls.get_by_id(user_id)

  if not user:
    return

  user_key = user.key

  to_delete = [user_key]

  # Delete UserQuestion.
  user_question_query = models.UserQuestion.query(
    models.UserQuestion.user == user_key)
  for user_question_key in user_question_query.iter(keys_only=True):
    to_delete.append(user_question_key)

  # Delete UserSeason.
  if not anonymous:
    user_season_query = models.UserSeason.query(
      models.UserSeason.user == user_key)
    for user_season_key in user_season_query.iter(keys_only=True):
      to_delete.append(user_season_key)

  ndb.delete_multi(to_delete)

  # Delete the user pic.
  if user.pic:
    blobstore.delete(user.pic)


class CleanUpAnonymousUsers(baserequesthandler.RequestHandler):
  """Delete anonymous users and user questions that are over a day old."""

  def get(self):
    yesterday = datetime.datetime.now() - datetime.timedelta(hours=24)
    q = models.AnonymousUser.query(
      models.AnonymousUser.joined < yesterday
    )
    more = True
    cursor = None
    while more:
      user_entities, next_cursor, more = q.fetch_page(
          BATCH_SIZE,
          start_cursor=cursor
      )
      for uq in user_entities:
        deferred.defer(delete_user, uq.key.id(), anonymous=True)


class CleanUpUserTokens(baserequesthandler.RequestHandler):
  """Delete User tokens that are older than 3 months old."""

  def get(self):
    # 'auth' Tokens expire after 3 months, 'bearer' after 1 year.
    now = datetime.datetime.utcnow()
    three_months_ago = now - datetime.timedelta(3 * (365/12))
    one_year_ago = now - datetime.timedelta(365)
    expired_tokens = UserToken.query(
      ndb.OR(ndb.AND(UserToken.subject == 'auth',
                     UserToken.created <= three_months_ago),
             ndb.AND(UserToken.subject == 'bearer',
                     UserToken.created <= one_year_ago))
    )

    while True:
      logging.info('Deleting user tokens')
      keys = expired_tokens.fetch(100, keys_only=True)
      if len(keys) > 0:
        ndb.delete_multi(keys)
      else:
        break


class ScheduledBackup(baserequesthandler.RequestHandler):

  def get(self):
    backup_folder = datetime.datetime.now().strftime('%y-%m-%d')
    bucket_name = 'ffcapp.appspot.com/backups/%s' % backup_folder
    params = {
      'filesystem' : 'gs',
      'gs_bucket_name': bucket_name,
      'kind' : BACKUP_ENTITIES
    }

    url = '/_ah/datastore_admin/backup.create'

    logging.info('Backing up %s to: %s' % (BACKUP_ENTITIES, bucket_name))
    taskqueue.add(url=url, params=params, queue_name='backup-builtin-queue')
