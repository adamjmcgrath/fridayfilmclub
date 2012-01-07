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



class Film(db.Model):
  """A Film.

  Attributes:
    title: The title of the Film.
    year: The year the Film came out.
  """
  title = db.StringProperty()
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
  clue_1 = db.TextProperty()
  clue_2 = db.TextProperty()
  clue_3 = db.TextProperty()
  film = db.ReferenceProperty(Film)
  posed = db.DateProperty()
  screenshot = blobstore.BlobReferenceProperty()
  updated = db.DateTimeProperty(auto_now=True)

  def screenshot_url(self, size=None):
    """Get's the question's screenshot url."""
    if self.screenshot:
      return images.get_serving_url(self.screenshot, size=size)
    else:
      return ''

  def clues(self):
    return [self.screenshot_url(), self.clue_1, self.clue_2, self.clue_3]


class User(db.Model):
  """A user.

  Attributes:
    films
  """
  user = db.UserProperty()


class Answer(db.Model):
  """Links user and question and keeps track of guesses and score.

  Attributes:
    question:
    user:
    guesses:
    score:
  """
  # @TODO (adamjmcgrath) Implement date answered correctly.
  answered_correctly = db.DateTimeProperty()
  correct = db.BooleanProperty()
  guess_0 = db.StringProperty() # Film db.Key.
  guess_1 = db.StringProperty() # Film db.Key.
  guess_2 = db.StringProperty() # Film db.Key.
  guess_3 = db.StringProperty() # Film db.Key.
  current_guess = db.IntegerProperty(default=0)
  incorrect = db.BooleanProperty()
  question = db.ReferenceProperty(Question, collection_name='answers')
  score = db.IntegerProperty()
  user = db.ReferenceProperty(User, collection_name='answers')

  def made_guesses(self):
    """Returns a list of guesses that have been made."""
    guesses = [self.guess_0, self.guess_1, self.guess_2, self.guess_3]
    return [Film.get(g).title for g in guesses if g != None]

  def required_clues(self):
    """Returns a list of clues that need to be shown to the user."""
    return self.question.clues()[:self.current_guess + 1]

  def calculate_score(self):
    """docstring for score"""
    # 0:10, 1:7, 2:5, 3:2
    scores = [10, 7, 5, 2]
    return scores[self.current_guess]

  def guess_is_correct(self, i):
    """Indicates wheather the guess is correct from a given index."""
    guess_key = getattr(self, ('guess_%d' % self.current_guess))
    return guess_key == self.question.film.key()
