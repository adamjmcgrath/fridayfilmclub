#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Api unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import sys
import unittest

from google.appengine.api import memcache
from google.appengine.ext import testbed

# TODO(adamjmcgrath) better way of including the src
sys.path.append('/Users/adammcgrath/dev/projects/ffc/src/')
sys.path.append('/Users/adammcgrath/dev/projects/ffc/src/lib/')
import api


class ApiTestCase(unittest.TestCase):

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_memcache_stub()

  def tearDown(self):
    self.testbed.deactivate()

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


if __name__ == '__main__':
    unittest.main()