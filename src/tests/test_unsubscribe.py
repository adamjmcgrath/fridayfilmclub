#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

"""Unsubscribe tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import unittest

import base
import helpers


class UnsubscribeTestCase(base.TestCase):

  def setUp(self):
    super(UnsubscribeTestCase, self).setUp()
    self.testbed.init_datastore_v3_stub()

  def testUnsubscribe(self):
    user = helpers.user(email='foo@bar.com', should_email=True)
    id = user.put().id()
    self.assertTrue(user.should_email)
    self.post('/unsubscribe/%d' % id, headers={'host': 'ffcapp.appspot.com'})
    self.assertFalse(user.should_email)

if __name__ == '__main__':
    unittest.main()