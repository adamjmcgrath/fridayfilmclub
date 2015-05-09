#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Auth unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import os
import sys
import unittest
import webtest
import webapp2
import webapp2_extras

from google.appengine.ext import testbed

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import base
import auth
import main
import models


class AuthTestCase(base.TestCase):

  def setUp(self):
    super(AuthTestCase, self).setUp()

    routes = [webapp2.Route('/', None, name='main')]
    app = webapp2.WSGIApplication(routes=routes, config=main.app_config)
    req = webapp2.Request.blank('/')
    req.app = app
    app.set_globals(app=main.app, request=req)
    self.req = req
    self.handler = auth.AuthHandler(request=req)
    session_store = webapp2_extras.sessions.SessionStore(req)
    self.session = session_store.get_session()
    self.handler.session_store = session_store

  def tearDown(self):
    self.testbed.deactivate()

  def testCreateNewGoogleUser(self):
    self.session['username'] = 'foo'

    auth_data = {
      'id': 'foo',
      'name': 'bar',
      'link': 'http://www.google.com',
      'email': 'quz@gmail.com',
      'refresh_token': 'quux'
    }
    self.handler._on_signin(auth_data, {}, 'google')
    user = models.User.get_by_username('foo')

    self.assertEqual(user.username, 'foo')
    self.assertEqual(user.name, 'bar')
    self.assertEqual(user.link, 'http://www.google.com')
    self.assertEqual(user.email, 'quz@gmail.com')
    self.assertEqual(user.google_name, 'bar')
    self.assertEqual(user.google_link, 'http://www.google.com')
    self.assertEqual(user.google_email, 'quz@gmail.com')
    self.assertEqual(user.refresh_token, 'quux')
    self.assertEqual(user.google_refresh_token, 'quux')
    self.assertIn('google:foo', user.auth_ids)

    messages = self.mail_stub.get_sent_messages(to='quz@gmail.com')
    self.assertEqual(1, len(messages))

  def testCreateNewFacebookUser(self):
    self.session['username'] = 'foo'

    auth_data = {
      'id': 'foo',
      'name': 'bar',
      'link': 'http://www.facebook.com',
      'email': 'quz@facebook.com'
    }
    self.handler._on_signin(auth_data, {}, 'facebook')
    user = models.User.get_by_username('foo')

    self.assertEqual(user.username, 'foo')
    self.assertEqual(user.name, 'bar')
    self.assertEqual(user.link, 'http://www.facebook.com')
    self.assertEqual(user.email, 'quz@facebook.com')
    self.assertEqual(user.facebook_name, 'bar')
    self.assertEqual(user.facebook_link, 'http://www.facebook.com')
    self.assertEqual(user.facebook_email, 'quz@facebook.com')
    self.assertEqual(user.facebook_uid, 'foo')
    self.assertIn('facebook:foo', user.auth_ids)

  def testCreateNewTwitterUser(self):
    self.session['username'] = 'foo'

    auth_data = {
      'id': 'foo',
      'screen_name': 'bar',
      'link': 'http://www.twitter.com'
    }
    auth_info = {
      'oauth_token': 'foo',
      'oauth_token_secret': 'bar'
    }
    self.handler._on_signin(auth_data, auth_info, 'twitter')
    user = models.User.get_by_username('foo')

    self.assertEqual(user.username, 'foo')
    self.assertEqual(user.name, 'bar')
    self.assertEqual(user.link, 'http://www.twitter.com')
    self.assertEqual(user.token, 'foo')
    self.assertEqual(user.token_secret, 'bar')
    self.assertIn('twitter:foo', user.auth_ids)

  def testExistingUser(self):
    existing_user = models.User(username='bar',
                                auth_ids=['google:foo'],
                                name='bar')
    existing_user.put()

    auth_data = {
      'id': 'foo',
      'name': 'baz'
    }
    self.handler._on_signin(auth_data, {}, 'google')
    user = models.User.get_by_username('bar')

    self.assertEqual(user.name, 'bar')
    self.assertEqual(user.google_name, 'baz')

  def testLoggedInUser(self):
    existing_user = models.User(username='bar',
                                auth_ids=['google:foo'],
                                name='bar')
    existing_user.put()
    self.handler.auth.set_session({
      'user_id': existing_user.key.id()
    })

    auth_data = {
      'id': 'bar'
    }
    self.handler._on_signin(auth_data, {}, 'facebook')
    user = models.User.get_by_username('bar')

    self.assertIn('google:foo', user.auth_ids)
    self.assertIn('facebook:bar', user.auth_ids)


if __name__ == '__main__':
    unittest.main()
