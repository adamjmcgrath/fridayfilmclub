#!/usr/bin/python
#
# Copyright 2014 Friday Film Club. All Rights Reserved.

"""Handles the realtime live scoring feature using the Channel API."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

from datetime import datetime, timedelta
import json
import logging

import baserequesthandler
from google.appengine.api import channel, memcache
from google.appengine.ext import deferred


def _send_score_to_players(user_key, user_question_score,
                           user_question_clues, user_season_score,
                           user_season_clues, user_season_answered):
  """Send a users score to all active players in a deferred."""
  user = user_key.get()
  channels = json.loads(memcache.get('channels') or '{}')
  msg = json.dumps({
    'user': user.username,
    'pic': user.pic_url(size=20),
    'score': user_question_score,
    'clues': user_question_clues,
    'season_score': user_season_score,
    'season_clues': user_season_clues,
    'season_answered': user_season_answered,
    'all_score': user.overall_score,
    'all_clues': user.overall_clues,
    'all_answered': user.questions_answered,
  })
  for client_id in channels.iterkeys():
    channel.send_message(client_id, msg)


def send_score_to_players(user, user_question, user_season):
  """Send a users score to all active players."""
  if not user_season:
    return

  # score, clues, answered
  deferred.defer(_send_score_to_players,
                 user.key,
                 user_question.score,
                 user_question.clues_used,
                 user_season.score,
                 user_season.clues,
                 user_season.questions_answered)


class Connect(baserequesthandler.RequestHandler):
  """Add the channel to memcache."""

  def post(self):
    client_id = self.request.get('from')
    channels = json.loads(memcache.get('channels') or '{}')
    channels[client_id] = str(datetime.now())
    memcache.set('channels', json.dumps(channels))


class Disconnect(baserequesthandler.RequestHandler):
  """Remove the channel from memcache."""

  def post(self):
    client_id = self.request.get('from')
    channels = json.loads(memcache.get('channels') or '{}')
    try:
      del channels[client_id]
      memcache.set('channels', json.dumps(channels))
    except KeyError:
      # No client found.
      pass
