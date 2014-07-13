#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

"""Async tasks for Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import datetime
import logging

from google.appengine.ext import deferred, blobstore, ndb

import baserequesthandler
import models

BATCH_SIZE = 100


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
