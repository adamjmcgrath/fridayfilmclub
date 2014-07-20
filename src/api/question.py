#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Question and Answer API - this contains the main quiz logic."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging

from datetime import datetime
import json

import baserequesthandler
import models
import realtime
import settings
import leaderboard

from google.appengine.api import users, urlfetch
from google.appengine.ext import deferred, ndb

_MAX_CLUES = 4
_PASS = 'pass'


class Question(baserequesthandler.RequestHandler):
  """The main question/answer app logic - through a REST api."""

  def get(self, question_id):
    self.get_or_post(question_id)

  def post(self, question_id):
    # Get the users guess
    guess = self.request.get('guess')

    self.get_or_post(question_id, guess=guess)

  def get_or_post(self, question_id, guess=None):

    # Get the question and user.
    question = models.Question.get_by_id(int(question_id))
    posed = question.posed
    anonymous_user = self.request.get('anonymous_user')
    user = self.current_user if self.logged_in else None

    # For debugging - create an arbitrary posed date for un-posed questions.
    if not posed:
      if users.is_current_user_admin():
        posed = datetime.now()
      else:
        return self.error(401)

    # If anonymous user, use the uid from the url. Only logged in users can
    # view the current question.
    if anonymous_user and not question.is_current:
      user = models.AnonymousUser.get_by_id(anonymous_user)

    if not user:
      return self.error(401)

    # Construct/get the user key.
    user_question_id = '%s-%s' % (question_id, user.key.id())
    user_question = models.UserQuestion.get_or_insert(
        user_question_id,
        question=question.key,
        user=user.key,
        user_is_admin=user.is_admin)

    to_put = []
    # Check if guess is correct, update UserQuestion.
    if guess and not user_question.complete:
      user_question.correct = (guess.strip() == str(question.answer_id))
      user_question.guesses.append(guess)
      num_guesses = len(user_question.guesses)

      if user_question.correct or num_guesses >= _MAX_CLUES:
        user_question.complete = True
        user_question.score = user_question.calculate_score(posed)
        user.overall_score += user_question.score
        user.overall_clues += num_guesses - 1
        user.questions_answered += 1
        question.answered += 1
        to_put.append(question)
        # Delete leaderboard memcache when a new score for the current
        # question comes in.
        if question.is_current:
          deferred.defer(leaderboard.delete_leaderboard_cache)

        if question.season and not user.is_anonymous:
          user_season_id = '%s-%s' % (question.season.id(), user.key.id())
          user_season = models.UserSeason.get_or_insert(user_season_id,
            season=question.season, user=user.key, user_is_admin=user.is_admin)
          user_season.score += user_question.calculate_score(posed)
          user_season.clues += num_guesses - 1
          user_season.questions_answered += 1
          to_put.append(user_season)
          if question.is_current or settings.DEBUG:
            realtime.send_score_to_players(user, user_question, user_season)

      to_put.append(user_question)
      to_put.append(user)
      if user.is_anonymous:
        user_question.put()
      else:
        ndb.put_multi(to_put)

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
        url = 'http://films-data.appspot.com/api?id=' + g
        film_dict = json.loads(urlfetch.fetch(url=url, follow_redirects=False).content)
        guesses.append({
          'title': film_dict['title'],
          'year': str(film_dict['year'])
        })

    response_obj = {
        'clues': [clue.get().to_json() for clue in question.clues[:clue_number]],
        'correct': user_question.correct,
        'guesses': guesses,
        'score': user_question.score or user_question.calculate_score(posed),
        'user': models.User.to_leaderboard_json(user)
    }

    # If the question is complete, reveal the correct answer to the user.
    if user_question.complete:
      response_obj['answer'] = {
        'key': question.answer_id,
        'title': question.answer_title,
        'year': question.answer_year,
      }
      response_obj['packshot'] = question.packshot_url(size=150)
      response_obj['imdb_url'] = question.imdb_url

    self.render_json(response_obj)
