#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Api unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import datetime
import mock
import os
import unittest

import base
import helpers
import models
import tasks

from google.appengine.ext import deferred, ndb


class TasksTestCase(base.TestCase):

  def testDeleteUser(self):
    user = helpers.user()
    user_id = user.put().id()
    self.assertTrue(bool(models.User.get_by_id(user_id)))
    tasks.delete_user(user_id)
    self.assertFalse(bool(models.User.get_by_id(user_id)))

  def testDeleteUserItems(self):
    user = helpers.user()
    user_key = user.put()
    to_put = []

    for i in range(5):
      to_put.append(helpers.user_question(user=user_key))
      to_put.append(helpers.user_season(user=user_key))

    ndb.put_multi(to_put)
    self.assertEqual(models.UserQuestion.query().count(), 5)
    self.assertEqual(models.UserSeason.query().count(), 5)

    tasks.delete_user(user_key.id())
    self.assertEqual(models.UserQuestion.query().count(), 0)
    self.assertEqual(models.UserSeason.query().count(), 0)

  @mock.patch.object(deferred, 'defer')
  def testDeleteAnonymousUsers(self, deferred_mock):
    users = []
    joined = datetime.datetime.now() - datetime.timedelta(hours=48)

    def side_effect(deffered_fun, *args, **kwargs):
      return deffered_fun(*args, **kwargs)
    deferred_mock.side_effect = side_effect

    for i in range(5):
      user = helpers.anonymous_user()
      user.joined = joined
      user.put()

    ndb.put_multi(users)
    self.assertEqual(models.AnonymousUser.query().count(), 5)

    os.environ['USER_IS_ADMIN'] = '1'
    self.get('/tasks/cleanupanonymoususers')
    self.assertEqual(models.AnonymousUser.query().count(), 0)


if __name__ == '__main__':
    unittest.main()
