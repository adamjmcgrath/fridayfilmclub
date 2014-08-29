#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

"""Usersearch unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import unittest

from google.appengine.api import search
from google.appengine.ext import ndb

import base
import helpers
import usersearch


class TasksTestCase(base.TestCase):

  def setUp(self):
    super(TasksTestCase, self).setUp()
    self.testbed.init_search_stub()

  def testTokenise(self):
    tests = [
      ('foo', ['f', 'fo', 'foo', 'o', 'oo']),
      ('b a r', ['a', 'b', 'r']),
      ('ba z', ['a', 'b', 'ba', 'z']),
    ]
    for test in tests:
      self.assertEqual(sorted(usersearch.tokenize(test[0])), test[1])

  def testIndexUsers(self):
    users = [
      helpers.user(id='foo', username='foo'),
      helpers.user(id='bar', username='bar'),
    ]
    ndb.put_multi(users)
    usersearch.index_users(users)
    index = search.Index(name='users')
    self.assertIsNotNone(index.get('foo'))
    self.assertIsNotNone(index.get('bar'))
    usersearch.remove_users([u.key for u in users])
    self.assertIsNone(index.get('foo'))
    self.assertIsNone(index.get('bar'))

if __name__ == '__main__':
    unittest.main()