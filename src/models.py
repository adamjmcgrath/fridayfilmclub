#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Friday Film Club models."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import datetime
import logging
import hashlib
import re
import time
import uuid

from webapp2_extras.appengine.auth.models import User as AuthUser

from google.appengine.api import files, images, urlfetch
from google.appengine.ext import ndb

import settings

RE_SPECIAL_CHARS_ = re.compile(r'[^a-zA-Z0-9 ]')

# Maximum possible score
_MAX_SCORE = 20000
# No. of seconds penalty per guess
_TIME_PER_PENALTY = 2000
WEEKS_PER_SEASON = 12

def slugify(my_string):
  """Remove special characters and replace spaces with hyphens."""
  return '-'.join(re.sub(RE_SPECIAL_CHARS_, '', my_string).lower().split(' '))



class Season(ndb.Model):
  """Group questions into seasons."""
  number = ndb.IntegerProperty()

  @staticmethod
  def get_current():
    season, week = Question.get_current_season_week()
    return Season.get_by_id(str(season))


# pylint: disable=W0232
class Question(ndb.Model):
  """A question.

  Attributes:
    answer:
    clues:
  """
  clues = ndb.KeyProperty(repeated=True)
  created = ndb.DateTimeProperty(auto_now_add=True)
  answer_id = ndb.StringProperty()
  answer_title = ndb.StringProperty()
  answer_year = ndb.IntegerProperty()
  posed = ndb.DateTimeProperty()
  updated = ndb.DateTimeProperty(auto_now=True)
  is_current = ndb.BooleanProperty(default=False)
  imdb_url = ndb.StringProperty()
  packshot = ndb.BlobKeyProperty()
  email_msg = ndb.TextProperty()
  season = ndb.KeyProperty(kind=Season)
  week = ndb.IntegerProperty()
  answered = ndb.IntegerProperty(default=0)

  def clue_image_url(self, size=None, crop=False):
    clue = self.clues[0]
    if clue:
      return clue.get().image_url(size=size, crop=crop)
    else:
      return None

  def packshot_url(self, size=None, crop=False):
    """Gets the packshot url."""
    if self.packshot:
      return images.get_serving_url(self.packshot, size=size, crop=crop)
    else:
      return ''

  def errors(self):
    """Checks that the question is ready to send."""
    errors = []
    if not self.clue_image_url():
      errors.append('Missing screenshot.')
    if not self.answer_id:
      errors.append('Missing answer.')
    if self.posed:
      errors.append('Already posed.')
    if not self.imdb_url or 'XXX' in self.imdb_url:
      errors.append('Missing IMDB url.')
    if not self.packshot_url():
      errors.append('Missing Packshot.')
    if not self.email_msg:
      errors.append('Missing Email Message.')
    return errors

  @staticmethod
  def get_current():
    """ Given a question, get the next one. """
    return Question.query(Question.is_current == True).get()

  @staticmethod
  def get_next():
    """ Given a question, get the next one. """
    season, week = Question.get_next_season_week()
    return Question.query(Question.season == ndb.Key('Season', str(season)),
                          Question.week == week).get()

  @staticmethod
  def get_current_season_week():
    q = Question.query(Question.is_current == True).get()
    if q:
      return q.season.get().number, q.week
    else:
      return 1, 0

  @staticmethod
  def get_next_season_week():
    (season, week) = Question.get_current_season_week()
    week += 1
    if week > WEEKS_PER_SEASON: #  12 weeks per season
      season += 1
      week = 1
    return season, week


# pylint: disable=W0232
class Clue(ndb.Model):
  """A clue."""
  text = ndb.TextProperty()
  image = ndb.BlobKeyProperty()
  question = ndb.KeyProperty(kind=Question)

  def image_url(self, size=None, crop=False):
    """Gets the image's url."""
    if self.image:
      return images.get_serving_url(self.image, size=size, crop=crop)
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
  is_admin = ndb.BooleanProperty(default=False)
  is_anonymous = ndb.BooleanProperty(default=False)
  pic = ndb.BlobKeyProperty()
  name = ndb.StringProperty()
  username = ndb.StringProperty()
  username_lower = ndb.ComputedProperty(lambda self: self.username.lower())
  favourite_film_id = ndb.StringProperty()
  favourite_film_title = ndb.StringProperty()
  favourite_film_year = ndb.IntegerProperty()
  link = ndb.StringProperty()
  google_avatar_url = ndb.StringProperty()
  google_name = ndb.StringProperty()
  google_link = ndb.StringProperty()
  google_refresh_token = ndb.StringProperty()
  facebook_avatar_url = ndb.StringProperty()
  facebook_name = ndb.StringProperty()
  facebook_link = ndb.StringProperty()
  facebook_uid = ndb.StringProperty()
  twitter_avatar_url = ndb.StringProperty()
  twitter_name = ndb.StringProperty()
  twitter_link = ndb.StringProperty()
  twitter_token = ndb.StringProperty()
  twitter_token_secret = ndb.StringProperty()
  overall_score = ndb.IntegerProperty(default=0)
  overall_clues = ndb.IntegerProperty(default=0)
  questions_answered = ndb.IntegerProperty(default=0)
  invited_by = ndb.KeyProperty(kind='User')
  joined = ndb.DateTimeProperty(auto_now_add=True)

  def pic_url(self, size=None, crop=False):
    """Gets the image's url."""
    if self.pic:
      return images.get_serving_url(self.pic, size=size, crop=crop)
    else:
      return ''

  def get_score_dict(self, score, season_score, overall_score):
    """Gets a dictionary for realtime scores."""
    return {
      'user': self.username,
      'pic': self.pic_url(size=20),
      'score': score,
      'season_score': season_score,
      'overall_score': overall_score
    }

  @staticmethod
  def get_by_username(username):
    return User.query().filter(User.username_lower == username.lower()).get()

  @staticmethod
  def blob_from_url(url):
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      file_name = files.blobstore.create(mime_type='application/octet-stream')
      with files.open(file_name, 'a') as f:
        f.write(result.content)
      files.finalize(file_name)
      return files.blobstore.get_blob_key(file_name)

  @staticmethod
  def to_leaderboard_json(user):
    """Used to return json for the leader board api all."""
    return {
      'user_name': user.username,
      'user_pic': user.pic_url(size=30),
      'score': user.overall_score,
      'clues': user.overall_clues,
      'answered': user.questions_answered,
    }


class AnonymousUser(User):
  is_anonymous = ndb.BooleanProperty(default=True)

  @classmethod
  def get(cls, existing_user_id=None):
    user_id = str(existing_user_id or uuid.uuid4())
    username = 'User-%s' % user_id
    return cls.get_or_insert(user_id, username=username)


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
  completed = ndb.DateTimeProperty(auto_now=True)
  correct = ndb.BooleanProperty(default=False)
  created = ndb.DateTimeProperty(auto_now_add=True)
  guesses = ndb.StringProperty(repeated=True)
  clues_used = ndb.ComputedProperty(lambda self: max(len(self.guesses) - 1, 0))
  question = ndb.KeyProperty(kind=Question)
  score = ndb.IntegerProperty()
  user = ndb.KeyProperty()  # Can be an anonymous user.
  user_is_admin = ndb.BooleanProperty(default=False)
  user_is_anonymous = ndb.BooleanProperty(default=False)

  def incorrect_guesses(self):
    if self.correct:
      return self.guesses[:-1]
    else:
      return self.guesses

  def calculate_score(self, posed):
    now = int(UserQuestion.now().strftime('%s'))
    posed = int(posed.strftime('%s'))
    penalties = len(self.incorrect_guesses()) * _TIME_PER_PENALTY
    if self.complete and not self.correct:
      score = 0
    else:
      score = max(_MAX_SCORE - (now - posed) - penalties, 0)

    logging.info('Score: Now: %d, Posed: %d, Penalties: %d, Score: %d', now,
        posed, penalties, score)

    return score

  @staticmethod
  def get_profile_dict(uq):
    """Great a dictionary for use in the profile scoreboard."""
    q = uq.question.get()
    return {
      'week': q.week,
      'season': q.season.id(),
      'score': uq.score,
      'guesses': uq.guesses
    }

  @staticmethod
  def to_leaderboard_json(user_question):
    """Used to return json for the leader board api all."""
    user = user_question.user.get()
    return {
      'user_name': user.username,
      'user_pic': user.pic_url(size=30),
      'score': user_question.score,
      'clues': len(user_question.guesses) - 1
    }

  @staticmethod
  def now():
    return datetime.datetime.now()


class UserSeason(ndb.Model):
  """Keep track of a users score over a season."""
  score = ndb.IntegerProperty(default=0)
  clues = ndb.IntegerProperty(default=0)
  season = ndb.KeyProperty(kind=Season)
  user = ndb.KeyProperty(kind=User)
  user_is_admin = ndb.BooleanProperty(default=False)
  questions_answered = ndb.IntegerProperty(default=0)

  @staticmethod
  def to_leaderboard_json(questions_in_season, user_season):
    """Used to return json for the leader board api season."""
    user = user_season.user.get()
    return {
      'user_name': user.username,
      'user_pic': user.pic_url(size=30),
      'score': user_season.score,
      'clues': user_season.clues,
      'answered': user_season.questions_answered,
    }