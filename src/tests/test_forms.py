#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

"""Forms unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import json
import mock
import unittest
import webapp2

from google.appengine.ext import ndb
from wtforms import validators, Form, FormField

import base
import helpers
import main
import forms


class FormsTestCase(base.TestCase):

  def setUp(self):
    super(FormsTestCase, self).setUp()
    routes = [webapp2.Route('/', None, name='main')]
    app = webapp2.WSGIApplication(routes=routes, config=main.app_config)
    req = webapp2.Request.blank('/')
    req.app = app
    app.set_globals(app=main.app, request=req)
    self.req = req
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_blobstore_stub()

  def testValidateValidUsername(self):
    field = mock.MagicMock()

    # Shouldn't raise an exception
    field.data = 'foo'
    forms.validate_username(None, field)
    field.data = 'foo_bar'
    forms.validate_username(None, field)
    field.data = '123'
    forms.validate_username(None, field)
    field.data = 'foo123'
    forms.validate_username(None, field)
    field.data = ' foo123 '
    forms.validate_username(None, field)

  def testValidateInvalidUsername(self):
    field = mock.MagicMock()

    field.data = 'fo'
    self.assertRaises(
      validators.ValidationError, forms.validate_username, None, field)

    field.data = 'foooooooooooooooo'
    self.assertRaises(
      validators.ValidationError, forms.validate_username, None, field)

    field.data = 'foo bar'
    self.assertRaises(
      validators.ValidationError, forms.validate_username, None, field)

  def testValidateExistingUsername(self):
    field = mock.MagicMock()
    helpers.user(username='foo').put()

    field.data = 'foo'
    self.assertRaises(
      validators.ValidationError, forms.validate_username, None, field)

  def testValidateValidLeagueName(self):
    form = mock.MagicMock()
    form.data = {'id': None}
    field = mock.MagicMock()

    # Shouldn't raise an exception
    field.data = 'foo'
    forms.validate_league_name(form, field)
    field.data = 'foo_bar'
    forms.validate_league_name(form, field)
    field.data = '123'
    forms.validate_league_name(form, field)
    field.data = 'foo123'
    forms.validate_league_name(form, field)
    field.data = ' foo123 '
    forms.validate_league_name(form, field)

  def testValidateInvalidLeagueName(self):
    form = mock.MagicMock()
    form.data = {'id': None}
    field = mock.MagicMock()

    field.data = ''
    self.assertRaises(
      validators.ValidationError, forms.validate_league_name, form, field)

  def testValidateExistingLeagueName(self):
    form = mock.MagicMock()
    field = mock.MagicMock()
    helpers.league(id=1, name='foo').put()
    helpers.league(id=2, name='bar').put()

    # No validation error if changing name of existing form.
    field.data = 'foo'
    form.data = {'id': 1}
    forms.validate_league_name(form, field)

    # No validation error if changing name of existing form.
    field.data = 'foo'
    form.data = {'id': 2}
    self.assertRaises(
      validators.ValidationError, forms.validate_league_name, form, field)

  def testFilmFieldProcess(self):
    field = forms.FilmField().bind(Form(), 'a')
    field.process_formdata([None])
    self.assertEqual(field.data, '')

    field.process_formdata(['/en/top_gun'])
    self.assertEqual(field.data['title'], 'Top Gun')

  def testFilmFieldPopulate(self):
    field = forms.FilmField().bind(Form(), 'a')
    field.data = {
      'key': 'foo',
      'year': 'bar',
      'title': 'baz',
    }
    obj = mock.MagicMock()
    field.populate_obj(obj, 'foo')
    self.assertEqual(obj.foo_id, 'foo')
    self.assertEqual(obj.foo_year, 'bar')
    self.assertEqual(obj.foo_title, 'baz')

  # def testImageFieldPopulate(self):
  #   field = forms.ImageField().bind(Form(), 'a')
  #   self.req.GET['foo'] = 'bar'
  #   obj = mock.MagicMock()
  #   field.populate_obj(obj, 'baz')
  #   self.assertIsNotNone(obj.baz)

  def testClueFieldListProcessNoClues(self):
    field_list = forms.CluesFieldList(FormField()).bind(Form(), 'a')
    field_list.process({})
    self.assertListEqual(field_list.data, [])

  def testWeekField(self):
    field = forms.WeekField().bind(Form(), 'a')
    obj = mock.MagicMock()
    field.data = '1'
    field.populate_obj(obj, 'foo')
    self.assertEqual(obj.week, 1)
    self.assertEqual(forms.WeekField.week_choices()[0], ('1', '1'))

  def testLeagueUserFieldProcess(self):
    field = forms.LeagueUsersField().bind(Form(), 'a')
    keys = [ndb.Key('User', 1), ndb.Key('User', 2)]
    field.process_data(keys)
    self.assertEqual(field.data, '1,2')

  def testLeagueUserPopulate(self):
    field = forms.LeagueUsersField().bind(Form(), 'a')
    obj = mock.MagicMock()
    field.data = '1,2'
    field.populate_obj(obj, 'foo')
    self.assertListEqual(obj.users, [ndb.Key('User', 1), ndb.Key('User', 2)])

  def testLeagueFormUsersJson(self):
    form = forms.League()
    form.users.data = str(helpers.user(username='foo').put().id())
    self.assertEqual(json.loads(form.users_json())[0]['username'], 'foo')


if __name__ == '__main__':
    unittest.main()