#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Friday Film Club models."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging

import webapp2
from google.appengine.api import files
from google.appengine.api import images
from google.appengine.api.datastore_errors import BadArgumentError
from google.appengine.ext import db
from google.appengine.ext import blobstore
from wtforms import fields, Form, validators

import settings


def slugify(st):
  """Remove special characters and replace spaces with hyphens."""
  return '-'.join(
      ''.join([s for s in st if (s.isalnum() or s == ' ')]).lower().split(' '))


class Film(db.Model):
  """A Film.

  Attributes:
    batch: An id for identifiying in which group the film was added.
    grossing: The dallar amount the film made.
    title: The title of the Film.
    title_slug: The slugified title of the Film.
    year: The year the Film came out.
  """
  batch = db.IntegerProperty()
  grossing = db.IntegerProperty()
  title = db.StringProperty()
  title_slug = db.StringProperty()
  year = db.IntegerProperty()

  def to_dict(self):
    return db.to_dict(self, {'key': str(self.key())})


class FilmIndex(db.Model):
  """An index to search for Films.

  Attributes:
    films: a list of films that the index matches.
  """
  films = db.ListProperty(db.Key)


class Question(db.Model):
  """A question.

  Attributes:
    answer:
    clues:
  """
  created = db.DateTimeProperty(auto_now_add=True)
  answer = db.ReferenceProperty(Film)
  posed = db.DateProperty()
  screenshot = blobstore.BlobReferenceProperty()
  updated = db.DateTimeProperty(auto_now=True)


class Clue(db.Model):
  """A clue."""
  text = db.TextProperty()
  image = blobstore.BlobReferenceProperty()
  question = db.ReferenceProperty(Question, collection_name='clues')

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


class User(db.Model):
  """A user.

  Attributes:
    films
  """
  user = db.UserProperty()


class UserQuestion(db.Model):
  """Links user and question and keeps track of guesses and score.

  Attributes:
    question:
    user:
    guesses:
    score:
  """
  # @TODO (adamjmcgrath) Implement date answered correctly.
  answered_correctly = db.DateTimeProperty()
  complete = db.BooleanProperty(default=False)
  correct = db.BooleanProperty(default=False)
  guesses = db.StringListProperty()
  current_guess = db.IntegerProperty(default=0)
  incorrect = db.BooleanProperty()
  question = db.ReferenceProperty(Question, collection_name='answers')
  score = db.IntegerProperty()
  user = db.ReferenceProperty(User, collection_name='answers')

  def calculate_score(self):
    """docstring for score"""
    # 0:10, 1:7, 2:5, 3:2
    scores = [10, 7, 5, 2]
    return scores[self.current_guess]
