#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Api unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import datetime
import json
import mock
import unittest

import base
from api import question as question_api
import helpers
import models


class ApiTestCase(base.TestCase):

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

  def testQuestionAllowsAnonymousUser(self):
    question = helpers.question(posed=datetime.datetime.now())
    user = helpers.anonymous_user(user_id='foo')
    user.put()
    response = self.get(
      '/api/question/%d?anonymous_user=%s' % (question.put().id(), 'foo'),
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
                                clues=helpers.clues(clues),
                                answer_title='Foo')
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
    self.assertEqual(response['answer']['title'], 'Foo')
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
    season = helpers.season()
    question = helpers.question(
      answer_id=answer,
      posed=datetime.datetime.now(),
      season=season.put()
    )
    user = helpers.user()
    question_id = question.put().id()
    guess = {
      'guess': answer
    }
    self.assertEqual(user.overall_score, 0)
    response = json.loads(self.post('/api/question/%d' % question_id,
                                    user=user, params=guess).body)
    self.assertTrue(response['correct'])
    self.assertTrue(response['answer']['title'], 'Top Gun')
    user_season = models.UserSeason.query(
        models.UserSeason.user == user.key,
        models.UserSeason.season == season.key).get()
    self.assertGreater(user_season.score, 0)
    self.assertGreater(user.overall_score, 0)

  @mock.patch('models.UserQuestion.now')
  def testUserSeason(self, now_mock):
    posed_date = datetime.datetime(2014, 1, 1, 0, 0, 0)
    now_mock.return_value = posed_date
    answer = '/en/top_gun'
    question = helpers.question(
      answer_id=answer,
      posed=posed_date,
      season=helpers.season().put()
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

    user_season_id = '%s-%s' % (question.season.id(), user.key.id())
    user_season = models.UserSeason.get_by_id(user_season_id)

    self.assertIsNotNone(user_season)
    self.assertEquals(user_season.score, 20000)
    self.assertEquals(user_season.clues, 0)
    self.assertEquals(user_season.questions_answered, 1)

  @mock.patch('models.UserQuestion.now')
  def testScoring(self, now_mock):
    posed_date = datetime.datetime(2014, 1, 1, 10, 0, 0)
    now_mock.return_value = datetime.datetime(2014, 1, 1, 11, 0, 0)
    question = helpers.question(
      posed=posed_date
    )
    user = helpers.user()
    question_id = question.put().id()
    guess = {
      'guess': 'pass'
    }
    response = json.loads(self.post('/api/question/%d' % question_id,
                                    user=user, params=guess).body)

    self.assertEquals(response['score'], 20000 - 2000 - (60 * 60))

  def testUpdateQuestion(self):
    question = helpers.question(answered=5)
    question_api.update_question(question)
    self.assertEqual(question.answered, 6)

  def testUpdateUserScore(self):
    user = helpers.user(
      overall_score=10,
      overall_clues=10,
      questions_answered=10,
      active_questions_answered=5,
    )
    question_api.update_users_score(user, 5, 5, True)
    self.assertEqual(user.overall_score, 15)
    self.assertEqual(user.overall_clues, 14)
    self.assertEqual(user.questions_answered, 11)
    self.assertEqual(user.active_questions_answered, 6)

  def testUpdateUsersLeagueScore(self):
    user = helpers.user()
    user_key = user.put()
    league = helpers.league(owner=user_key)
    league_key = league.put()
    user.leagues = [league_key]
    user.put()
    league_user_id = '%s-%s' % (league_key.id(), user_key.id())
    league_user = helpers.league_user(id=league_user_id,
                                      user=user_key,
                                      league=league_key,
                                      score=5,
                                      clues=5,
                                      questions_answered=1)
    league_user.put()
    question_api.update_users_league_scores(user_key, 5, 5, False)
    self.assertEqual(league_user.score, 10)
    self.assertEqual(league_user.clues, 9)
    self.assertEqual(league_user.questions_answered, 2)

if __name__ == '__main__':
    unittest.main()
