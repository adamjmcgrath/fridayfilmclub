#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2014 Friday Film Club. All Rights Reserved.

"""Get season stats.
"""

import getpass
import json
import logging
import operator
import os
import sys
import urllib

APPENGINE_PATH = '/usr/local/google_appengine/'

def fix_appengine_path():
  EXTRA_PATHS = [
    APPENGINE_PATH,
    os.path.join(APPENGINE_PATH, 'lib', 'antlr3'),
    os.path.join(APPENGINE_PATH, 'lib', 'django'),
    os.path.join(APPENGINE_PATH, 'lib', 'fancy_urllib'),
    os.path.join(APPENGINE_PATH, 'lib', 'ipaddr'),
    os.path.join(APPENGINE_PATH, 'lib', 'webapp2'),
    os.path.join(APPENGINE_PATH, 'lib', 'webob-1.1.1'),
    os.path.join(APPENGINE_PATH, 'lib', 'yaml', 'lib'),
    os.path.join(APPENGINE_PATH, 'lib', 'webapp2-2.5.2'),
  ]
  sys.path.extend(EXTRA_PATHS)

fix_appengine_path()

# Add models to path.
sys.path.insert(0, '/Users/adammcgrath/dev/projects/ffc/src/')

from google.appengine.ext import ndb
from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.api.files import records
from google.appengine.datastore import entity_pb
from google.appengine.api import datastore


import models

APP_NAME = 's~ffcapp'
os.environ['AUTH_DOMAIN'] = 'gmail.com'
os.environ['USER_EMAIL'] = 'adamjmcgrath@gmail.com'


def auth_func():
  return os.environ['USER_EMAIL'], getpass.getpass('Password:')


def incorrect_guesses():
  questions = {}
  question_titles = {}
  count = 10
  for uq in models.UserQuestion.query():
    count += 1
    try:
      questions[question_titles[uq.question.id()]] += uq.guesses
    except KeyError:
      title = uq.question.get().answer_title
      question_titles[uq.question.id()] = title
      questions[title] = uq.guesses
    print uq.key.id()

  f = open('season.json', 'w')
  f.write(json.dumps(questions, indent=2))
  f.close()


def incorrect_guesses_report():
  questions = json.loads(open('season.json').read())
  for title, guesses in questions.items():
    ranked_guesses = {}
    for g in guesses:
      try:
        ranked_guesses[g] += 1
      except:
        ranked_guesses[g] = 1
    print title
    sorted_guesses = sorted(ranked_guesses.iteritems(), key=operator.itemgetter(1), reverse=True)
    count = 0
    for sg in sorted_guesses:
      count +=1
      if sg[0] != 'pass':
        url = 'http://films-data.appspot.com/api?id=' + sg[0]
        film_dict = json.loads(urllib.urlopen(url).read())
        print '\t%s: %s' % (film_dict['title'], sg[1])
      if count == 7:
        break


def film_year_report():
  for q in models.Question.query():
    if q.season:
      print '%s: %d' % (q.answer_title, q.answer_year)


def question_difficulty():
  questions = {}
  question_titles = {}
  count = 0
  for uq in models.UserQuestion.query():
    count += 1
    try:
      questions[question_titles[uq.question.id()]] += uq.clues_used
    except KeyError:
      title = uq.question.get().answer_title
      question_titles[uq.question.id()] = title
      questions[title] = uq.clues_used

  print questions

def main():
  # Use 'localhost:8080' for dev server.
  remote_api_stub.ConfigureRemoteDatastore(APP_NAME, '/_ah/remote_api',
      auth_func, servername='ffcapp.appspot.com')

  # incorrect_guesses()
  # incorrect_guesses_report()
  # film_year_report()
  question_difficulty()

if __name__ == '__main__':
  main()
