#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Api unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import datetime
import json
import os
import sys
import unittest
import webtest
import webapp2

from google.appengine.api import memcache

import api
import base
import helpers
import models


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

  def testQuestionRequiresAdminOrPosed(self):
    question = helpers.question()
    user = helpers.user()
    response = self.get('/api/question/%d' % question.put().id(),
                        user=user)
    self.assertEqual(response.status_int, 401)

  def testQuestionRequiresAdmin(self):
    question = helpers.question()
    user = helpers.user(is_admin=True)
    response = self.get('/api/question/%d' % question.put().id(),
                        user=user)
    self.assertEqual(response.status_int, 200)

  def testQuestionRequiresPosed(self):
    question = helpers.question(posed=datetime.datetime.now())
    user = helpers.user()
    response = self.get('/api/question/%d' % question.put().id(),
                        user=user)
    self.assertEqual(response.status_int, 200)

  def testCreateUserQuestion(self):
    question = helpers.question(posed=datetime.datetime.now())
    user = helpers.user()
    question_id = question.put().id()
    self.get('/api/question/%d' % question_id, user=user)

    user_question_id = '%s-%s' % (question_id, user.key.id())
    self.assertIsNotNone(models.UserQuestion.get_by_id(user_question_id))

  def testQuestionStartResponse(self):
    question = helpers.question(posed=datetime.datetime.now())
    user = helpers.user()
    question_id = question.put().id()
    response = self.get('/api/question/%d' % question_id, user=user)
    response_dict = json.loads(response.body)

    # self.assertAlmostEqual(response_dict['score'], 20000)
    self.assertEqual(len(response_dict['guesses']), 0)
    self.assertEqual(len(response_dict['clues']), 0)
    self.assertFalse(response_dict['correct'])

  def testQuestionPass(self):
    clues = ['foo', 'bar', 'baz', 'qux']
    question = helpers.question(posed=datetime.datetime.now(),
                                clues=helpers.clues(clues))
    user = helpers.user()
    question_id = question.put().id()
    response = self.post('/api/question/%d' % question_id,
                         user=user,
                         params={'guess': 'pass'})
    response_dict = json.loads(response.body)

    print response



if __name__ == '__main__':
    unittest.main()