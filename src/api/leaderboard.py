#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

"""Leaderboard API."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging

from functools import partial
import json

import baserequesthandler
import models


from google.appengine.api import memcache
from google.appengine.ext import ndb


# Property map for normalising sorting across the different model.
_PROP_MAP = {
  'all': {
    'score': 'overall_score',
    'clues': 'overall_clues',
    'answered': 'questions_answered'
  },
  'week': {
    'score': 'score',
    'clues': 'clues_used'
  },
  'season': {
    'score': 'score',
    'clues': 'clues',
    'answered': 'questions_answered',
  }
}
_LB_CACHE = 'leaderboard_cache'


def set_leaderboard_cache(key, value, existing_cache=''):
  """Set the leaderboard cache."""
  if not existing_cache:
    existing_cache = memcache.get(_LB_CACHE) or ''
  cache_keys = existing_cache.split('|')
  cache_keys.append(key)
  memcache.set_multi({
    key: value,
    _LB_CACHE: '|'.join(cache_keys)
  })


def delete_leaderboard_cache():
  """Delete the leaderboard cache."""
  mc = memcache.Client()
  lb_cache = mc.get(_LB_CACHE)
  if lb_cache:
    mc.delete_multi(lb_cache.split('|') + [_LB_CACHE])


class LeaderBoard(baserequesthandler.RequestHandler):
  """Leader boards."""

  def get(self, duration):
    is_all = duration == 'all'
    is_week = duration == 'week'
    offset = int(self.request.get('offset') or 0)
    limit = int(self.request.get('limit') or 20)
    try:
      sort_props = _PROP_MAP[duration]
    except KeyError:
      sort_props = _PROP_MAP['season']
    sort = self.request.get('sort') or 'score'
    direction = self.request.get('dir') or 'asc'
    league_param = self.request.get('league')
    league = None

    cache_key = '%s:%s:%s:%s:%s' % (str(duration), str(offset),
                                    str(limit), sort, direction)

    if league_param:
      league = models.League.get_by_id(int(league_param))
      cache_key += ':%s' % league_param

    cached = memcache.get_multi([_LB_CACHE, cache_key])
    if cached.get(cache_key) and (cache_key in cached.get(_LB_CACHE, '')):
      self.render_json(cached.get(cache_key), is_string=True)
      return

    sort_prop = ndb.GenericProperty(sort_props[sort])
    if not direction == 'asc':
      sort_prop = -sort_prop

    # To get the min max range of the values get a value either side of the
    # query. If the offset is 0 the min is the first value.
    min_offset = 1 if offset else 0
    qo = ndb.QueryOptions(offset=offset - min_offset,
                          limit=limit + 1 + min_offset)

    if is_all:
      user_query = models.User.query(
        models.User.is_admin == False).order(sort_prop)
      if league:
        user_query = user_query.filter(models.User._key.IN(league.users))
      count = user_query.count()
      users_dicts = user_query.map(models.User.to_leaderboard_json, options=qo)

    elif is_week:
      question_query = models.Question.query(
          models.Question.is_current == True)

      question_key = question_query.get(keys_only=True)
      user_question_query = models.UserQuestion.query(
          models.UserQuestion.question == question_key,
          models.UserQuestion.complete == True,
          models.UserQuestion.user_is_admin == False).order(sort_prop)
      if league:
        user_question_query = user_question_query.filter(
          models.UserQuestion.user.IN(league.users))
      count = user_question_query.count()
      users_dicts = user_question_query.map(
          models.UserQuestion.to_leaderboard_json, options=qo)

    else: # Should be the Season number.
      season = models.Season.get_by_id(duration)
      user_season_query = models.UserSeason.query(
          models.UserSeason.season == season.key,
          models.UserSeason.user_is_admin == False).order(sort_prop)
      if league:
        user_season_query = user_season_query.filter(
          models.UserSeason.user.IN(league.users))
      questions_in_season = models.Question.query(
          models.Question.season == season.key).count()
      count = user_season_query.count()
      users_dicts = user_season_query.map(
          partial(models.UserSeason.to_leaderboard_json, questions_in_season),
          options=qo)

    json_str = json.dumps({
      'prev': users_dicts and users_dicts[0].get(sort) or 0,
      'next': users_dicts and users_dicts[-1].get(sort) or 0,
      'users': users_dicts[min_offset:][:limit],
      'count': count
    })
    set_leaderboard_cache(cache_key, json_str,
                          existing_cache=cached.get(_LB_CACHE, ''))
    self.render_json(json_str, is_string=True)