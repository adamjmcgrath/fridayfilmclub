#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Api unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import datetime
import os
import sys
import unittest
import webtest
import webapp2

from google.appengine.api import memcache


import api
import base
import helpers

class ApiTestCase(base.TestCase):

  def setUp(self):
    super(ApiTestCase, self).setUp()
    self.testbed.init_datastore_v3_stub()

  def testLeaderBoardSetCache(self):
    api.set_leaderboard_cache('foo', 'bar')
    self.assertEqual(memcache.get('foo'), 'bar')
    self.assertEqual(memcache.get(api._LB_CACHE), '|foo')

    api.set_leaderboard_cache('bar', 'baz')
    self.assertEqual(memcache.get('bar'), 'baz')
    self.assertEqual(memcache.get(api._LB_CACHE), '|foo|bar')

  def testLeaderBoardSetCacheWithExisting(self):
    api.set_leaderboard_cache('foo', 'bar', existing_cache='qux|quux')
    self.assertEqual(memcache.get('foo'), 'bar')
    self.assertEqual(memcache.get(api._LB_CACHE), 'qux|quux|foo')

  def testLeaderBoardDeleteCache(self):
    api.set_leaderboard_cache('bar', 'baz')
    api.set_leaderboard_cache('foo', 'bar')
    api.delete_leaderboard_cache()
    self.assertEqual(memcache.get('foo'), None)
    self.assertEqual(memcache.get('bar'), None)
    self.assertEqual(memcache.get(api._LB_CACHE), None)

  def testHandlers(self):
    question = helpers.question()
    user = helpers.user()
    response = self.get('/api/question/%d' % question.put().id(),
                        user=user)

    self.assertEqual(response.status_int, 200)


if __name__ == '__main__':
    unittest.main()