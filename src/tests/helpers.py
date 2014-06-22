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

def question(clues=[],
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
  return models.Question(**locals())


def user(is_admin=None,
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
         joined=None):
  return models.User(**locals())


def clue(text=None,
         image=None,
         question=None):
  return models.Clue(**locals())


def clues(clue_list):
  return map(lambda c: clue(text=c).put(), clue_list)


def season(number=1):
  return models.Season(**locals())