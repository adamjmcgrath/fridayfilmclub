#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Base unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import os
import sys
import unittest
import webtest
import webapp2
import webapp2_extras
from webapp2_extras.securecookie import SecureCookieSerializer

SUPER_SECRET = 'my-super-secret'

from google.appengine.ext import ndb, testbed

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import main


class TestCase(unittest.TestCase):

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.app = webapp2.WSGIApplication(config={
      'webapp2_extras.sessions': {
          'cookie_name': '_simpleauth_sess',
          'secret_key': SUPER_SECRET
      },
      'webapp2_extras.auth': {
        'user_attributes': [],
        'cookie_name': '_simpleauth_sess',
      }
    }, routes=main.routes)
    self.testapp = webtest.TestApp(self.app)

  def tearDown(self):
    self.testbed.deactivate()
    ndb.get_context().clear_cache()
    os.environ['USER_EMAIL'] = ''
    os.environ['USER_IS_ADMIN'] = ''

  def log_user_in(self, user):
    user_id = user.put().id()
    session = {
      '_user': [
        user_id,
        False,
        webapp2_extras.appengine.auth.models.User.create_auth_token(user_id),
        0,
        0
      ]
    }
    secure_cookie_serializer = SecureCookieSerializer(
        SUPER_SECRET
    )
    serialized = secure_cookie_serializer.serialize(
        '_simpleauth_sess', session
    )
    os.environ['USER_IS_ADMIN'] = '1' if user.is_admin else '0'
    os.environ['USER_EMAIL'] = '' if user.is_anonymous else user.email

    return {'Cookie': '_simpleauth_sess=%s' % serialized}

  def get(self, url, user=None, params=None):
    headers = {}

    if user:
      headers = self.log_user_in(user)

    return self.testapp.get(url,
                            headers=headers,
                            expect_errors=True,
                            params=params)

  def post(self, url, user=None, headers=None, **kwargs):
    headers = headers or {}

    if user:
      headers = dict(headers.items() + self.log_user_in(user).items())

    return self.testapp.post(url,
                             headers=headers,
                             expect_errors=True,
                             **kwargs)


if __name__ == '__main__':
    unittest.main()