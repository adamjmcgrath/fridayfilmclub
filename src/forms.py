#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Friday Film Club models."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

from cgi import escape
import datetime
import logging
import json
import re
import posixpath

import webapp2
from webapp2_extras import auth
from google.appengine.api import files
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from google.appengine.ext.db import BadKeyError
from wtforms import fields, Form, validators, widgets

import models
import settings


_USERNAME_RE = re.compile(r'^[\w\d_]{3,16}$')

def validate_username(form, field):
  """Validate the username."""
  auth_obj = auth.get_auth()
  user_dict = auth_obj.get_user_by_session()
  original_username = None
  if user_dict:
    user = auth_obj.store.user_model.get_by_id(user_dict['user_id'])
    original_username = user.username

  username = field.data.strip()

  if not _USERNAME_RE.search(username):
    raise validators.ValidationError('Invalid username.')

  # Only throw a name already exists error, if the user is trying to change their username.
  elif (username != original_username) and models.User.get_by_username(username):
    raise validators.ValidationError('This username is already taken.')


class FilmField(fields.HiddenField):
  """A film field."""

  def process_formdata(self, valuelist):
    """Process data received over the wire from a form."""
    film_key = valuelist and valuelist[0]
    if not film_key:
      self.data = ''
    else:
      try:
        url = 'http://films-data.appspot.com/api?id=' + film_key
        self.data = json.loads(urlfetch.fetch(url=url, follow_redirects=False).content)
      except BadKeyError:
        self.data = ''

  def populate_obj(self, obj, name):
    """Populate the object represented by the film field."""
    if self.data:
      setattr(obj, name + '_id', self.data['key'])
      setattr(obj, name + '_year', self.data['year'])
      setattr(obj, name + '_title', self.data['title'])


class ImageField(fields.FileField):
  """An image field."""

  def populate_obj(self, obj, name):
    """Populate the object represented by the film field."""
    req = webapp2.get_request()
    img_file = req.get(self.name)
    if not img_file:
      return
    file_name = files.blobstore.create(mime_type='application/octet-stream')
    with files.open(file_name, 'a') as f:
      f.write(img_file)
    files.finalize(file_name)

    setattr(obj, name, files.blobstore.get_blob_key(file_name))


class ClueForm(Form):
  """A clue form."""
  text = fields.TextAreaField('Text')
  image = ImageField('Image')


class ClueFormField(fields.FormField):

  def populate_obj(self, entity):
    """docstring for populate_obj"""

    self.form.populate_obj(entity)


class CluesFieldList(fields.FieldList):

  def process(self, formdata, obj=None, **kwargs):
    if obj:
      clues = [clue.get() for clue in obj]
      super(CluesFieldList, self).process(formdata, clues, **kwargs)
    else:
      super(CluesFieldList, self).process(formdata, **kwargs)

  def populate_obj(self, entity, name):
    counter = 0

    for entry, data in zip(self.entries, self.data):
      try:
        clue = entity.clues[counter].get()
        entry.populate_obj(clue)
        clue.put()
      except IndexError:
        clue_id = '%d-%d' % (entity.key.id(), counter)
        clue = models.Clue(id=clue_id, question=entity.key)
        entry.populate_obj(clue)
        clue.put()
        entity.clues.append(clue.key)
      counter += 1

class WeekField(fields.SelectField):

  def populate_obj(self, entity, name):
    entity.week = int(self.data)

  @staticmethod
  def week_choices():
    return [(str(x), str(x)) for x in range(1, models.WEEKS_PER_SEASON + 1)]

  @staticmethod
  def week_default():
    return models.Question.get_next_season_week()[1]


class SeasonField(fields.SelectField):

  def populate_obj(self, entity, name):
    season = self.data
    entity.season = models.Season.get_or_insert(season, number=int(season)).key

  @staticmethod
  def season_choices():
    season, week = models.Question.get_next_season_week()
    return [(str(x), str(x)) for x in range(season, season + 10)]


class Question(Form):
  """A question form."""
  answer = FilmField('Film', [validators.Required()], id='film')
  clues = CluesFieldList(ClueFormField(ClueForm), min_entries=4)
  email_msg = fields.TextAreaField('Email Message')
  packshot = ImageField('Image')
  imdb_url = fields.TextField('IMDB Link',
                              default='http://www.imdb.com/title/XXX/')
  week = WeekField(choices=WeekField.week_choices(),
                   default=WeekField.week_default())
  season = SeasonField(choices=SeasonField.season_choices())


class Registration(Form):
  """The registration form."""
  username = fields.TextField('', [validate_username])


class User(Form):
  username = fields.TextField('', [validate_username])
  email = fields.TextField(validators=[validators.Email()])
  pic = ImageField('pic')
  favourite_film = FilmField()
