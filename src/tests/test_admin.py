#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Api unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import datetime
import os
import json
import mock
import unittest
import webtest

import base
import helpers
import admin
import models


class AdminTestCase(base.TestCase):

  def setUp(self):
    super(AdminTestCase, self).setUp()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_mail_stub()
    self.mail_stub = self.testbed.get_stub('mail')

  def testGetQuestionUrl(self):
    prod_host = 'http://ffc.appspot.com/'
    local_host = 'http://localhost:8080/'
    question = 'foo'

    self.assertEqual(admin.get_question_url(prod_host, question),
                     'http://www.fridayfilmclub.com/question/foo')

    self.assertEqual(admin.get_question_url(local_host, question),
                     'http://localhost:8080/question/foo')

    self.assertEqual(admin.get_question_url(prod_host, question, dev=True),
                     'http://dev.ffcapp.appspot.com/question/foo')

    self.assertEqual(admin.get_question_url(local_host, question, dev=True),
                     'http://localhost:8080/question/foo')

  def testPoseQuestionEmail(self):
    helpers.user(email='foo@bar.com').put()
    os.environ['USER_IS_ADMIN'] = '1'
    self.post('/admin/posequestion', params={
      'subject': 'Foo',
      'msg': 'Bar',
      'question': 'baz',
    }, headers={'host': 'ffcapp.appspot.com'})

    messages = self.mail_stub.get_sent_messages(to='foo@bar.com')
    message = messages[0]
    self.assertEqual(1, len(messages))
    self.assertEqual('Foo', message.subject)
    self.assertIn(
      'http://www.fridayfilmclub.com/question/baz', message.body.payload)

  def testPoseQuestionTrustedTesterEmail(self):
    helpers.user(email='foo@bar.com', is_trusted_tester=True).put()
    os.environ['USER_IS_ADMIN'] = '1'
    self.post('/admin/posequestion', params={
      'subject': 'Foo',
      'msg': 'Bar',
      'question': 'baz',
    }, headers={'host': 'ffcapp.appspot.com'})

    messages = self.mail_stub.get_sent_messages(to='foo@bar.com')
    message = messages[0]
    self.assertEqual(1, len(messages))
    self.assertEqual('Foo', message.subject)
    self.assertIn(
      'http://dev.ffcapp.appspot.com/question/baz', message.body.payload)

  def testPoseQuestionNoEmail(self):
    helpers.user(email=None).put()
    os.environ['USER_IS_ADMIN'] = '1'
    self.post('/admin/posequestion', params={
      'subject': 'Foo',
      'msg': 'Bar',
      'question': 'baz',
    }, headers={'host': 'ffcapp.appspot.com'})

    messages = self.mail_stub.get_sent_messages()
    self.assertEqual(0, len(messages))


  def testAddQuestion(self):
    helpers.user(email='foo@bar.com', is_trusted_tester=True).put()
    os.environ['USER_IS_ADMIN'] = '1'
    self.post('/admin/addquestion', params={
      'answer': '/en/the_lost_boys',
      'season': '1',
      'week': '3',
      'clues-0-image': webtest.Upload('screenshot.jpg', 'screenshot contents'),
      'clues-1-text': 'clue 1',
      'clues-2-text': 'clue 2',
      'clues-3-text': 'clue 3',
      'email_msg': 'My email message',
      'imdb_url': 'http://www.imdb.com/title/foo/',
      'packshot': webtest.Upload('packshot.jpg', 'packshot contents'),
    }, headers={'host': 'ffcapp.appspot.com'})
    question = models.Question.query().get()
    season = models.Season.query().get()
    clues = models.Clue.query().fetch(3)

    self.assertEqual('The Lost Boys', question.answer_title)
    self.assertEqual(1, season.number)
    self.assertEqual(3, question.week)
    self.assertIn('/_ah/img/encoded_gs_file:', question.packshot_url())
    self.assertIn('/_ah/img/encoded_gs_file:', question.clue_image_url())
    self.assertEquals(3, len(clues))
    self.assertEquals('My email message', question.email_msg)
    self.assertEquals('http://www.imdb.com/title/foo/', question.imdb_url)


if __name__ == '__main__':
    unittest.main()