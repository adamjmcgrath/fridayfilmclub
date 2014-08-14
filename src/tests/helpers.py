#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Api unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import datetime
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

import models


def question(clues=None,
             answer_id='foo',
             answer_title='bar',
             answer_year=2000,
             posed=None,
             is_current=False,
             imdb_url='http://imdb.com',
             packshot=None,
             email_msg='Message',
             season=None,
             week=1,
             answered=0):
  clues = clues or []
  return models.Question(**locals())


def user(id=None,
         is_admin=None,
         is_trusted_tester=None,
         pic=None,
         name='John Smith',
         username='johnsmith',
         email='johnsmith@example.com',
         favourite_film_id='topgun',
         favourite_film_title='Top Gun',
         favourite_film_year=1998,
         link='http://www.google.com',
         overall_score=0,
         overall_clues=0,
         questions_answered=0,
         invited_by=None,
         joined=None,
         leagues=None):
  leagues = leagues or []
  return models.User(**locals())


def user_question(complete=False,
                  completed=None,
                  correct=False,
                  created=None,
                  guesses=None,
                  question=None,
                  score=None,
                  user=None,
                  user_is_admin=False,
                  user_is_anonymous=False):
  guesses = guesses or []
  return models.UserQuestion(**locals())


def user_season(score=None,
                clues=None,
                season=None,
                user=None,
                user_is_admin=None,
                questions_answered=None):
  return models.UserSeason(**locals())


def league(name='Foo',
           owner=None,
           users=None,
           created=None):
  users = users or []
  return models.League(**locals())


def league_user(id=None,
                created=None,
                user=None,
                league=None,
                score=None,
                clues=None,
                questions_answered=None):
  return models.LeagueUser(**locals())


def anonymous_user(user_id=None):
  return models.AnonymousUser.get(existing_user_id=user_id)


def clue(text=None,
         image=None,
         question=None):
  return models.Clue(**locals())


def clues(clue_list):
  return map(lambda c: clue(text=c).put(), clue_list)


def season(id=None, number=1):
  return models.Season(**locals())