#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Friday Film Club models."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

from datetime import datetime
import logging
import re

from webapp2_extras.appengine.auth.models import User as AuthUser

from google.appengine.api import images
from google.appengine.ext import ndb


RE_SPECIAL_CHARS_ = re.compile(r'[^a-zA-Z0-9 ]')

# Maximum possible score
_MAX_SCORE = 10000
# No. of seconds penalty per guess
_TIME_PER_PENALTY = 1000


def slugify(my_string):
  """Remove special characters and replace spaces with hyphens."""
  return '-'.join(re.sub(RE_SPECIAL_CHARS_, '', my_string).lower().split(' '))



class Film(ndb.Model):
  """A Film.

  Attributes:
    batch: An id for identifiying in which group the film was added.
    grossing: The dallar amount the film made.
    title: The title of the Film.
    title_slug: The slugified title of the Film.
    year: The year the Film came out.
  """
  batch = ndb.IntegerProperty()
  grossing = ndb.IntegerProperty()
  title = ndb.StringProperty()
  title_slug = ndb.StringProperty()
  year = ndb.IntegerProperty()

  def to_dict(self):
    return {
      'key': self.key.string_id(),
      'batch': self.batch,
      'grossing': self.grossing,
      'title': self.title,
      'title_slug': self.title_slug,
      'year': self.year,
    }


class FilmIndex(ndb.Model):
  """An index to search for Films.

  Attributes:
    films: a list of films that the index matches.
  """
  films = ndb.KeyProperty(repeated=True)


# pylint: disable=W0232
class Question(ndb.Model):
  """A question.

  Attributes:
    answer:
    clues:
  """
  clues = ndb.KeyProperty(repeated=True)
  created = ndb.DateTimeProperty(auto_now_add=True)
  answer = ndb.KeyProperty(kind=Film)
  posed = ndb.DateTimeProperty()
  updated = ndb.DateTimeProperty(auto_now=True)
  is_current = ndb.BooleanProperty(default=False)


# pylint: disable=W0232
class Clue(ndb.Model):
  """A clue."""
  text = ndb.TextProperty()
  image = ndb.BlobKeyProperty()
  question = ndb.KeyProperty(kind=Question)

  def image_url(self, size=None):
    """Gets the image's url."""
    if self.image:
      return images.get_serving_url(self.image, size=size)
    else:
      return ''

  def to_json(self):
    return {
      'text': self.text,
      'image': self.image_url(),
    }


# pylint: disable=W0232
class User(AuthUser):
  """A user.

  Attributes:
    films
  """
  avatar_url = ndb.StringProperty()
  name = ndb.StringProperty()
  link = ndb.StringProperty()
  google_avatar_url = ndb.StringProperty()
  google_name = ndb.StringProperty()
  google_link = ndb.StringProperty()
  facebook_avatar_url = ndb.StringProperty()
  facebook_name = ndb.StringProperty()
  facebook_link = ndb.StringProperty()
  twitter_avatar_url = ndb.StringProperty()
  twitter_name = ndb.StringProperty()
  twitter_link = ndb.StringProperty()
  overall_score = ndb.IntegerProperty(default=0)
  questions_answered = ndb.IntegerProperty(default=0)

  @staticmethod
  def to_leaderboard_json(user):
    """Used to return json for the leader board api all."""
    return {
      'user_name': user.name,
      'user_pic': user.avatar_url,
      'score': user.overall_score,
      'answered': user.questions_answered,
    }


# pylint: disable=W0232
class UserQuestion(ndb.Model):
  """Links user and question and keeps track of guesses and score.

  Attributes:
    question:
    user:
    guesses:
    score:
  """
  complete = ndb.BooleanProperty(default=False)
  correct = ndb.BooleanProperty(default=False)
  guesses = ndb.StringProperty(repeated=True)
  question = ndb.KeyProperty(kind=Question)
  score = ndb.IntegerProperty()
  user = ndb.KeyProperty(kind=User)

  def incorrect_guesses(self):
    if self.correct:
      return self.guesses[:-1]
    else:
      return self.guesses

  def calculate_score(self, posed):
    now = int(datetime.now().strftime('%s'))
    posed = int(posed.strftime('%s'))
    penalties = len(self.incorrect_guesses()) *  _TIME_PER_PENALTY
    if self.complete and not self.correct:
      score = 0
    else:
      score = max(_MAX_SCORE - (now - posed) - penalties, 0)

    logging.info('Score: Now: %d, Posed: %d, Penalties: %d, Score: %d', now,
        posed, penalties, score)

    return score

  @staticmethod
  def to_leaderboard_json(user_question):
    """Used to return json for the leader board api all."""
    user = user_question.user.get()
    return {
      'user_name': user.name,
      'user_pic': user.avatar_url,
      'score': user_question.score,
      'answered': user.questions_answered,
    }

