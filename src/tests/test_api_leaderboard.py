#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Api unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import datetime
import json
import mock
import unittest

from google.appengine.api import memcache
from google.appengine.ext import ndb

import base
from api import leaderboard
import helpers
import models


class ApiTestCase(base.TestCase):

  def setUp(self):
    super(ApiTestCase, self).setUp()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    to_put = []
    question = helpers.question(is_current=True, clues=[])
    question_key = question.put()
    user = helpers.user()
    user_key = user.put()
    league = helpers.league(owner=user_key)
    self.league_key = league.put()
    # Remove the league user object that the league creates for the owner.
    models.LeagueUser.query().get().key.delete()
    season = helpers.season(id='5', number=5)
    season_key = season.put()
    for i in range(20):
      to_put.append(helpers.user(
          is_admin=False,
          username='user-%d' % i,
          overall_score=i,
          overall_clues=i,
          questions_answered=i))
      to_put.append(helpers.user_question(
          user_is_admin=False,
          complete=True,
          question=question_key,
          user=user_key,
          guesses=[str(ii) for ii in range(i)],
          score=i))
      to_put.append(helpers.league_user(
          league=self.league_key,
          user=user_key,
          score=i,
          clues=i,
          questions_answered=i))
      to_put.append(helpers.user_season(
          score=i,
          clues=i,
          season=season_key,
          user=user_key,
          user_is_admin=False,
          questions_answered=i))
    ndb.put_multi(to_put)

  def testLeaderboardSetCache(self):
    leaderboard.set_leaderboard_cache('foo', 'bar')
    self.assertEqual(memcache.get('foo'), 'bar')
    self.assertEqual(memcache.get(leaderboard._LB_CACHE), '|foo')

    leaderboard.set_leaderboard_cache('bar', 'baz')
    self.assertEqual(memcache.get('bar'), 'baz')
    self.assertEqual(memcache.get(leaderboard._LB_CACHE), '|foo|bar')

  def testLeaderboardSetCacheWithExisting(self):
    leaderboard.set_leaderboard_cache('foo', 'bar', existing_cache='qux|quux')
    self.assertEqual(memcache.get('foo'), 'bar')
    self.assertEqual(memcache.get(leaderboard._LB_CACHE), 'qux|quux|foo')

  def testLeaderboardDeleteCache(self):
    leaderboard.set_leaderboard_cache('bar', 'baz')
    leaderboard.set_leaderboard_cache('foo', 'bar')
    leaderboard.delete_leaderboard_cache()
    self.assertEqual(memcache.get('foo'), None)
    self.assertEqual(memcache.get('bar'), None)
    self.assertEqual(memcache.get(leaderboard._LB_CACHE), None)

  def testDefaultAllLeaderboard(self):
    response = self.get_json('/api/leaderboard/all')
    self.assertEqual(response['count'], 20)
    self.assertEqual(response['prev'], 0)
    self.assertEqual(response['next'], 19)
    self.assertEqual(len(response['users']), 20)
    self.assertEqual(response['users'][0]['score'], 0)
    self.assertEqual(response['users'][19]['score'], 19)

  def testAllLeaderboardDsc(self):
    response = self.get_json('/api/leaderboard/all?dir=dsc')
    self.assertEqual(response['prev'], 19)
    self.assertEqual(response['next'], 0)
    self.assertEqual(response['users'][0]['score'], 19)
    self.assertEqual(response['users'][19]['score'], 0)

  def testAllLeaderboardOffsetLimit(self):
    response = self.get_json('/api/leaderboard/all?dir=dsc&offset=5&limit=5')
    self.assertEqual(response['count'], 20)
    self.assertEqual(response['prev'], 15)
    self.assertEqual(response['next'], 9)
    self.assertEqual(response['users'][0]['score'], 14)
    self.assertEqual(len(response['users']), 5)

  def testAllLeaderboardAnswersSort(self):
    response = self.get_json('/api/leaderboard/all?dir=dsc&sort=answered')
    self.assertEqual(response['count'], 20)
    self.assertEqual(response['prev'], 19)
    self.assertEqual(response['next'], 0)
    self.assertEqual(response['users'][0]['answered'], 19)

  def testAllLeaderboardCache(self):
    response = self.get(
      '/api/leaderboard/all?dir=dsc&offset=5&limit=5&sort=clues')
    self.assertEqual(memcache.get('all:5:5:clues:dsc'), response.body)

  def testDefaultWeekLeaderboard(self):
    response = self.get_json('/api/leaderboard/week?dir=dsc&limit=1&sort=clues')
    self.assertEqual(response['count'], 20)
    self.assertEqual(response['prev'], 18)
    self.assertEqual(response['next'], 17)
    self.assertEqual(len(response['users']), 1)
    self.assertEqual(response['users'][0]['clues'], 18)

  def testDefaultLeagueLeaderboard(self):
    response = self.get_json(
      '/api/leaderboard/league?league=%d&dir=asc&sort=score' %
      self.league_key.id())
    self.assertEqual(response['count'], 20)
    self.assertEqual(response['prev'], 0)
    self.assertEqual(response['next'], 19)
    self.assertEqual(len(response['users']), 20)
    self.assertEqual(response['users'][0]['clues'], 0)

  def testLeagueLeaderboardCache(self):
    response = self.get(
        '/api/leaderboard/league?league=%d&dir=asc&sort=score' %
        self.league_key.id())
    self.assertEqual(
      memcache.get('league:0:20:score:asc:%d' % self.league_key.id()),
      response.body)

  def testSeasonLeaderboard(self):
    response = self.get_json(
      '/api/leaderboard/5?dir=dsc&sort=answered&offset=18&limit=2')
    self.assertEqual(response['count'], 20)
    self.assertEqual(response['prev'], 2)
    self.assertEqual(response['next'], 0)
    self.assertEqual(len(response['users']), 2)
    self.assertEqual(response['users'][0]['answered'], 1)


if __name__ == '__main__':
    unittest.main()