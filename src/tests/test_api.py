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

  @mock.patch('models.UserQuestion.now')
  def testQuestionStartResponse(self, now_mock):
    posed_date = datetime.datetime(2014, 1, 1, 0, 0, 0)
    now_mock.return_value = posed_date
    question = helpers.question(posed=posed_date)
    user = helpers.user()
    question_id = question.put().id()
    response = json.loads(
      self.get('/api/question/%d' % question_id, user=user).body)

    self.assertEqual(response['score'], 20000)
    self.assertEqual(len(response['guesses']), 0)
    self.assertEqual(len(response['clues']), 0)
    self.assertFalse(response['correct'])

  @mock.patch('models.UserQuestion.now')
  def testQuestionPass(self, now_mock):
    posed_date = datetime.datetime(2014, 1, 1, 0, 0, 0)
    now_mock.return_value = posed_date
    clues = ['foo', 'bar', 'baz', 'qux']
    question = helpers.question(posed=posed_date,
                                clues=helpers.clues(clues))
    user = helpers.user()
    pass_guess = {'guess': 'pass'}
    question_id = question.put().id()

    # Get question
    response = json.loads(
      self.get('/api/question/%d' % question_id, user=user).body)
    self.assertEqual(response['score'], 20000)
    self.assertEqual(len(response['guesses']), 0)
    self.assertEqual(len(response['clues']), 1)
    self.assertFalse(response['correct'])
    self.assertEqual(response['clues'][-1]['text'], 'foo')

    # 1st pass
    response = json.loads(self.post('/api/question/%d' % question_id,
                                    user=user, params=pass_guess).body)
    self.assertEqual(response['score'], 18000)
    self.assertEqual(len(response['guesses']), 1)
    self.assertEqual(len(response['clues']), 2)
    self.assertFalse(response['correct'])
    self.assertEqual(response['clues'][-1]['text'], 'bar')

    # 2nd pass
    response = json.loads(self.post('/api/question/%d' % question_id,
                                    user=user, params=pass_guess).body)
    self.assertEqual(response['score'], 16000)
    self.assertEqual(len(response['guesses']), 2)
    self.assertEqual(len(response['clues']), 3)
    self.assertFalse(response['correct'])
    self.assertEqual(response['clues'][-1]['text'], 'baz')

    # 3rd pass
    response = json.loads(self.post('/api/question/%d' % question_id,
                                    user=user, params=pass_guess).body)
    self.assertEqual(response['score'], 14000)
    self.assertEqual(len(response['guesses']), 3)
    self.assertEqual(len(response['clues']), 4)
    self.assertFalse(response['correct'])
    self.assertEqual(response['clues'][-1]['text'], 'qux')

    # 4th pass - question is complete.
    response = json.loads(self.post('/api/question/%d' % question_id,
                                    user=user, params=pass_guess).body)
    self.assertEqual(response['score'], 0)
    self.assertEqual(len(response['guesses']), 4)
    self.assertEqual(len(response['clues']), 4)
    self.assertFalse(response['correct'])

  def testGuess(self):
    question = helpers.question(posed=datetime.datetime.now())
    user = helpers.user()
    question_id = question.put().id()
    guess = {
      'guess': '/en/top_gun'
    }
    response = json.loads(self.post('/api/question/%d' % question_id,
                                    user=user, params=guess).body)
    self.assertEqual(response['guesses'][0]['title'], 'Top Gun')

  def testCorrect(self):
    answer = '/en/top_gun'
    question = helpers.question(
      answer_id=answer,
      posed=datetime.datetime.now()
    )
    user = helpers.user()
    question_id = question.put().id()
    guess = {
      'guess': answer
    }
    response = json.loads(self.post('/api/question/%d' % question_id,
                                    user=user, params=guess).body)
    self.assertTrue(response['correct'])
    self.assertTrue(response['answer']['title'], 'Top Gun')

if __name__ == '__main__':
    unittest.main()