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


def _send_score_to_players(from_user_key, score):
  """Send a users score to all active players in a deferred."""
  from_user = from_user_key.get()
  channels = json.loads(memcache.get('channels') or '{}')
  for client_id in channels.iterkeys():
    channel.send_message(client_id, json.dumps(from_user.get_score_dict(score)))


def send_score_to_players(from_user, score):
  """Send a users score to all active players."""
  deferred.defer(_send_score_to_players, from_user.key, score)


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
