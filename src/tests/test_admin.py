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

import base
import helpers
import admin


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


if __name__ == '__main__':
    unittest.main()