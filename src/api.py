#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Question and Answer API - this contains the main quiz logic."""

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
_PASS = 'pass'
# This is used to calculate the users score based on how many guesses they have
# had. If they get it on the first guess, they get the maximum points. It's not
# possible to get it right without guessing, so add a place holder at the front.
_SCORE = [None, 10, 7, 5, 2, 0]


class Question(baserequesthandler.RequestHandler):
  """Shows the homepage."""

  def get(self, question_key):
    return self.get_or_post(question_key)

  def post(self, question_key):
    # Get the users guess
    guess = self.request.get('guess')

    return self.get_or_post(question_key, guess=guess)

  def get_or_post(self, question_key, guess=None):

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
      if user_question.correct or len(user_question.guesses) >= _MAX_CLUES:
        user_question.complete = True
      user_question.put()

    # The number of the clues to show the user is one greater than the
    # number of guesses up to the maximum number of guesses.
    # If the user has had no guesses they get one clue.
    clue_increment = 0 if user_question.correct else 1
    clue_number = min((len(user_question.guesses) + clue_increment), _MAX_CLUES)

    guesses = []
    for g in user_question.guesses:
      if g == _PASS:
        # A blank guess is a "pass".
        guesses.append({})
      else:
        film_entity = models.Film.get(g)
        guesses.append({
          'title': film_entity.title,
          'year': str(film_entity.year)
        })

    response_obj = {
        'clues': [clue.to_json() for clue in question.clues[:clue_number]],
        'correct': user_question.correct,
        'guesses': guesses,
    }

    # If the question is complete, reveal the correct answer to the user.
    if user_question.complete:
      response_obj['answer'] = question.answer.to_dict()

    # Calculate the users score. Unless they have answered the question
    # correctly, their score is effectively the score they will get IF they
    # answer the next question correctly.
    index = len(user_question.guesses)
    if not user_question.correct:
      index += 1
    response_obj['score'] = _SCORE[index]

    return self.render_json(response_obj)

