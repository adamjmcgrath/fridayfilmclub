#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

"""LeagueUser unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import unittest

import base
import helpers
import models


class LeagueUserTestCase(base.TestCase):

  def testGetOrInsert(self):
    user_key = helpers.user().put()
    league_key = helpers.league(owner=user_key).put()
    league_user = models.LeagueUser.from_league_user(league_key, user_key)
    self.assertEqual(
      league_user.key,
      models.LeagueUser.key_from_league_user(league_key, user_key))

  def testToLeaderboardJson(self):
    user_key = helpers.user(username='foo').put()
    league_key = helpers.league(owner=user_key).put()
    league_user = models.LeagueUser.from_league_user(league_key, user_key)
    league_user.score = 1
    league_user.clues = 2
    league_user.questions_answered = 3
    league_user_json = models.LeagueUser.to_leaderboard_json(league_user)
    self.assertEqual(league_user_json['user_name'], 'foo')
    self.assertEqual(league_user_json['score'], 1)
    self.assertEqual(league_user_json['clues'], 2)
    self.assertEqual(league_user_json['answered'], 3)


if __name__ == '__main__':
    unittest.main()
