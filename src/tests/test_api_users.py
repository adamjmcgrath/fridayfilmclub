#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

"""Users API unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import unittest

from google.appengine.ext import ndb

import base
import helpers


class ApiTestCase(base.TestCase):

  def setUp(self):
    super(ApiTestCase, self).setUp()
    ndb.put_multi([
      helpers.user(username='foo'),
      helpers.user(username='bar'),
      helpers.user(username='baz'),
    ])

  def testUserSearch(self):
    response = self.get_json('/api/users/foo')
    self.assertEqual(len(response), 1)
    self.assertEqual(response[0]['username'], 'foo')

    response = self.get_json('/api/users/ba')
    self.assertEqual(len(response), 2)

if __name__ == '__main__':
    unittest.main()
