#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

"""Async tasks for Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import datetime
import logging

from google.appengine.ext import ndb

import baserequesthandler
import models

BATCH_SIZE = 100


class CleanUpAnonymousUsers(baserequesthandler.RequestHandler):
  """Delete anonymous users and user questions that are over an hour old."""

  def get(self):
    an_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    q = models.UserQuestion.query(
      models.UserQuestion.created < an_hour_ago,
      models.UserQuestion.user_is_anonymous == True
    )
    more = True
    cursor = None
    while more:
      to_delete = []
      user_question_entities, next_cursor, more = q.fetch_page(
          BATCH_SIZE,
          start_cursor=cursor
      )
      for uq in user_question_entities:
        to_delete += [uq.key, uq.user]
      ndb.delete_multi(to_delete)
