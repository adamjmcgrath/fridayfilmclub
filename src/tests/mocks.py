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
                   posed=datetime.datetime.now(),
                   is_current=True,
                   imdb_url='http://imdb.com',
                   packshot=None,
                   email_msg='Message',
                   # season=models.Season,
                   week=1,
                   answered=0):

  return models.Question(**locals())