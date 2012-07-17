#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Question and Answer API."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import json
import logging

import webapp2
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db

import forms
import models
import settings

_MAX_CLUES = 4


class Quiz(webapp2.RequestHandler):
  """Shows the homepage."""

  def post(self, question_key):
    # Get optional api settings.
    debug = self.request.get('debug')
    callback = self.request.get('callback')

    # Get the users guess
    guess = self.request.get('guess')

    # Get the question and user.
    question = models.Question.get(question_key)
    user_id = users.get_current_user().user_id()
    user_entity = models.User.get_by_key_name(user_id)

    # Construct/get the user key.
    user_question_key = posixpath.join(user_id, question_key)
    user_question = models.UserQuestion.get_or_insert(user_question_key,
      question=question, user=user_entity)

    # Check if guess is correct, update UserQuestion.
    if guess:
      user_question.correct = (guess.strip() == str(question.answer))
      user_question.guesses.append(guess)
      if user_question.correct or len(user_question.guesses) > _MAX_CLUES:
        user_question.complete = True
      user_question.put()

    # The number of the clues to show the user is one greater than the
    # number of guesses up to the maximum number of guesses.
    # If the user has had no guesses they get one clue.
    clue_number = max((len(user_question.guesses) + 1), _MAX_CLUES)

    response = {
      'correct': user_question.correct,
      'complete': user_question.complete,
      'guesses': user_question.guesses,
      'clues': question.clues[:clue_number],
    }

    # Create/format the json response.
    indent = 2 if debug else None
    json_response = json.dumps(response, indent=indent)
    if callback and settings._VALID_CALLBACK.match(callback):
      json_response = '%s(%s)' % (callback, json_response)

    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return webapp2.Response(json_response)

