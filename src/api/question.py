#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

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

_PASS = 'pass'


def update_question(question):
  question.answered += 1
  # Delete leaderboard memcache when a new score for the current
  # question comes in.
  if question.is_current:
    deferred.defer(leaderboard.delete_leaderboard_cache)


def update_users_score(user, score, num_guesses):
  user.overall_score += score
  user.overall_clues += num_guesses - 1
  user.questions_answered += 1


def update_users_season_score(user_season, score, num_guesses):
  user_season.score += score
  user_season.clues += num_guesses - 1
  user_season.questions_answered += 1


def update_users_league_scores(user_key, score, num_guesses):
  to_put = []
  user = user_key.get()
  for league_key in user.leagues:
    user_league = models.UserLeague.from_league_key_user(league_key, user_key)
    user_league.score += score
    user_league.clues += num_guesses - 1
    user_league.questions_answered += 1
    to_put.append(user_league)
  ndb.put_multi(to_put)


def populate_guess(guess_id):
  """Get the title and year of a guessed film from the films data API."""
  if guess_id == _PASS:
    # A blank guess is a "pass".
    return {}
  else:
    url = 'http://films-data.appspot.com/api?id=%s' % guess_id
    film_response = urlfetch.fetch(url=url, follow_redirects=False)
    film_dict = json.loads(film_response.content)
    return {
      'title': film_dict['title'],
      'year': str(film_dict['year'])
    }


class Question(baserequesthandler.RequestHandler):
  """The main question/answer app logic - through a REST api."""

  def get_user(self, question_is_current):
    anonymous_user = self.request.get('anonymous_user')
    user = self.current_user if self.logged_in else None
    # If anonymous user, use the uid from the url. Only logged in users can
    # view the current question.
    if anonymous_user and not question_is_current:
      user = models.AnonymousUser.get_by_id(anonymous_user)
    return user

  def get(self, question_id):
    self.get_or_post(question_id)

  def post(self, question_id):
    self.get_or_post(question_id)

  def get_or_post(self, question_id):
    guess = self.request.get('guess')

    # Get the question and user.
    question = models.Question.get_by_id(int(question_id))
    user = self.get_user(question.is_current)
    posed = question.posed or (users.is_current_user_admin() and datetime.now())
    to_put = []

    # Only posed questions with valid users can be shown.
    if not posed or not user:
      return self.error(401)

    # Construct/get the user key.
    user_question = models.UserQuestion.from_user_question(user, question)

    # Check if guess is correct, update UserQuestion.
    if guess and not user_question.complete:
      user_question.correct = (guess.strip() == str(question.answer_id))
      user_question.guesses.append(guess)
      num_guesses = len(user_question.guesses)
      complete = user_question.correct or num_guesses >= models._MAX_CLUES
      user_question.complete = complete

      if complete:
        score = user_question.calculate_score(posed)
        user_question.score = score
        user_season = None

        # Update the users score and stats.
        update_users_score(user, score, num_guesses)

        # Update the question answer count and reset the leaderboard cache.
        update_question(question)

        # Update the users leagues.
        if user.leagues:
          deferred.defer(update_users_league_scores,
                         user.key,
                         score,
                         num_guesses)

        # Update the user season.
        if question.season and not user.is_anonymous:
          season = question.season
          user_season = models.UserSeason.from_user_season(user, season)
          update_users_season_score(user_season, score, num_guesses)
          to_put.append(user_season)

        # If it's the current question, send the realtime score to the boards.
        if question.is_current or settings.DEBUG:
          realtime.send_score_to_players(user, user_question, user_season)

      # Only need to update the user question if anonymous as they don't appear
      # in the leaderboard.
      if user.is_anonymous:
        user_question.put()
      else:
        # Update the entities in the datastore.
        to_put += [question, user_question, user]
        ndb.put_multi(to_put)

    # Get the next set of guesses, clues to send to show to the user.
    guesses = map(populate_guess, user_question.guesses)
    clues = question.clues[:user_question.current_clue_number()]

    # Create the JSON for the UI.
    response_obj = {
        'clues': [c.get().to_json() for c in clues],
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
