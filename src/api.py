#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Question and Answer API."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import json
import logging
import posixpath

import webapp2
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db

import baserequesthandler
import forms
import models
import settings

_MAX_CLUES = 4


class Question(baserequesthandler.RequestHandler):
  """Shows the homepage."""

  def get(self, question_key):

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
    if guess and not user_question.complete:
      user_question.correct = (guess.strip() == str(question.answer.key()))

      user_question.guesses.append(guess)
      if user_question.correct or len(user_question.guesses) > _MAX_CLUES:
        user_question.complete = True
      user_question.put()

    # The number of the clues to show the user is one greater than the
    # number of guesses up to the maximum number of guesses.
    # If the user has had no guesses they get one clue.
    clue_increment = 0 if user_question.correct else 1
    clue_number = min((len(user_question.guesses) + clue_increment), _MAX_CLUES)

    try:
      guesses = models.Film.get(user_question.guesses)
    except db.BadKeyError:
      guesses = []

    # If the question is complete, reveal the correct answer to the user.
    answer = {}
    if user_question.complete:
      answer = question.answer.to_dict()

    return self.render_json({
        'answer': answer,
        'clues': [clue.to_json() for clue in question.clues[:clue_number]],
        'complete': user_question.complete,
        'correct': user_question.correct,
        'guesses': [{'title': g.title, 'year': str(g.year)} for g in guesses],
    })

