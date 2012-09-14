#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Friday Film Club models."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging
import re
import models

import webapp2
from webapp2_extras.appengine.auth.models import User as AuthUser

from google.appengine.api import files
from google.appengine.api import images
from google.appengine.api.datastore_errors import BadArgumentError
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from wtforms import fields, Form, validators

import settings

RE_SPECIAL_CHARS_ = re.compile(r'[^a-zA-Z0-9 ]')


def slugify(st):
  """Remove special characters and replace spaces with hyphens."""
  return '-'.join(re.sub(RE_SPECIAL_CHARS_, '', st).lower().split(' '))



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


class Question(ndb.Model):
  """A question.

  Attributes:
    answer:
    clues:
  """
  answers = ndb.KeyProperty(repeated=True)
  clues = ndb.KeyProperty(repeated=True)
  created = ndb.DateTimeProperty(auto_now_add=True)
  answer = ndb.KeyProperty(kind=Film)
  posed = ndb.DateProperty()
  updated = ndb.DateTimeProperty(auto_now=True)


class Clue(ndb.Model):
  """A clue."""
  text = ndb.TextProperty()
  image = ndb.BlobKeyProperty()
  question = ndb.KeyProperty(kind=Question)

  def image_url(self, size=None):
    """Get's the image's url."""
    if self.image:
      return images.get_serving_url(self.image, size=size)
    else:
      return ''

  def to_json(self):
    return {
      'text': self.text,
      'image': self.image_url(),
    }


# webapp2_extras.appengine.auth.models.User
class User(AuthUser):
  """A user.

  Attributes:
    films
  """
  user = ndb.UserProperty()
  answers = ndb.KeyProperty()


class UserQuestion(ndb.Model):
  """Links user and question and keeps track of guesses and score.

  Attributes:
    question:
    user:
    guesses:
    score:
  """
  # @TODO (adamjmcgrath) Implement date answered correctly.
  answered_correctly = ndb.DateTimeProperty()
  complete = ndb.BooleanProperty(default=False)
  correct = ndb.BooleanProperty(default=False)
  guesses = ndb.StringProperty(repeated=True)
  current_guess = ndb.IntegerProperty(default=0)
  incorrect = ndb.BooleanProperty()
  question = ndb.KeyProperty(kind=Question)
  score = ndb.IntegerProperty()
  user = ndb.KeyProperty(kind=User)

