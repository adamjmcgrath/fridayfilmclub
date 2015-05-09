#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

"""League unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import unittest

import base
import helpers
import models


class LeagueTestCase(base.TestCase):

  def testPostPutHook(self):
    league_owner = helpers.user()
    league_member_1 = helpers.user()
    league_member_2 = helpers.user()
    league = models.League(name='Foo',
                           owner=league_owner.put(),
                           users=[league_member_1.put(), league_member_2.put()])
    league_key = league.put()
    self.assertListEqual(league_owner.leagues, [league_key])
    self.assertListEqual(league_member_1.leagues, [league_key])
    self.assertListEqual(league_member_2.leagues, [league_key])

    league.users = [league_member_2.key]
    league.put()
    self.assertListEqual(league_member_1.leagues, [])
    self.assertListEqual(league_member_2.leagues, [league_key])

  def testPostDeleteHook(self):
    league_owner = helpers.user()
    league_member_1 = helpers.user()
    league_member_2 = helpers.user()
    league = models.League(name='Foo',
                           owner=league_owner.put(),
                           users=[league_member_1.put(), league_member_2.put()])
    league_key = league.put()
    self.assertListEqual(league_owner.leagues, [league_key])
    self.assertListEqual(league_member_1.leagues, [league_key])
    self.assertListEqual(league_member_2.leagues, [league_key])

    league.key.delete()
    self.assertListEqual(league_owner.leagues, [])
    self.assertListEqual(league_member_1.leagues, [])
    self.assertListEqual(league_member_2.leagues, [])

  def testGetByName(self):
    league = models.League(name='Foo',
                           owner=helpers.user().put())
    league.put()
    self.assertEqual(models.League.get_by_name('foo'), league)


if __name__ == '__main__':
    unittest.main()
