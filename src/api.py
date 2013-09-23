#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Question and Answer API - this contains the main quiz logic."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

from datetime import datetime
import logging

import auth
import baserequesthandler
import models

from google.appengine.api import users

_MAX_CLUES = 4
_PASS = 'pass'


class Question(baserequesthandler.RequestHandler):
  """Shows the homepage."""

  @auth.login_required
  def get(self, question_id):
    return self.get_or_post(question_id)

  @auth.login_required
  def post(self, question_id):
    # Get the users guess
    guess = self.request.get('guess')

    return self.get_or_post(question_id, guess=guess)

  def get_or_post(self, question_id, guess=None):

    # Get the question and user.
    question = models.Question.get_by_id(int(question_id))
    user = self.current_user
    posed = question.posed

    # For debugging - create an arbitrary posed date for un-posed questions.
    if not posed and users.is_current_user_admin():
      posed = datetime.now()

    # Construct/get the user key.
    user_question_id = '%s-%s' % (question_id, user.key.id())
    user_question = models.UserQuestion.get_or_insert(user_question_id,
      question=question, user=user)

    # Check if guess is correct, update UserQuestion.
    if guess and not user_question.complete:
      user_question.correct = (guess.strip() == str(question.answer.id()))

      user_question.guesses.append(guess)
      if user_question.correct or len(user_question.guesses) >= _MAX_CLUES:
        user_question.complete = True
        user_question.score = user_question.calculate_score(posed)
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
        film_entity = models.Film.get_by_id(g)
        guesses.append({
          'title': film_entity.title,
          'year': str(film_entity.year)
        })

    response_obj = {
        'clues': [clue.get().to_json() for clue in question.clues[:clue_number]],
        'correct': user_question.correct,
        'guesses': guesses,
        'score': user_question.calculate_score(posed)
    }

    # If the question is complete, reveal the correct answer to the user.
    if user_question.complete:
      response_obj['answer'] = question.answer.get().to_dict()

    return self.render_json(response_obj)

