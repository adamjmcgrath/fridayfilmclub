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
import cloudstorage

import webapp2
from webapp2_extras import auth
from google.appengine.api import images, urlfetch
from google.appengine.ext import blobstore, ndb
from google.appengine.ext.db import BadKeyError
from wtforms import fields, Form, validators, widgets

import models
import settings


_USERNAME_RE = re.compile(r'^[\w\d_]{3,16}$')
GCS_ROOT = '/ffcapp.appspot.com/images/'


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


def validate_league_name(form, field):
  """Validate the league name."""
  current_league_id = form.data['id']
  current_league_name = None
  if current_league_id:
    current_league = models.League.get_by_id(int(current_league_id))
    current_league_name = current_league.name

  league_name = field.data.strip()

  if not league_name:
    raise validators.ValidationError('No league name specified.')

  else:
    # Only throw a name already exists error, if the user is trying to
    # create a league or change their league name.
    if ((league_name != current_league_name) and
         models.League.get_by_name(models.slugify(league_name))):
      raise validators.ValidationError('League name already exists.')


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

  def __init__(self, name, gcs_folder, img_size=None, **kwargs):
    self.gcs_folder = gcs_folder
    self.img_size = img_size
    super(ImageField, self).__init__(name, **kwargs)

  def file_name(self, req, obj):
    img_file = req.POST.get(self.name)
    return img_file.filename

  def populate_obj(self, obj, name):
    """Populate the question model with a GCS image."""
    req = webapp2.get_request()
    if not req.get(self.name):
      return

    img_file = req.POST.get(self.name)
    file_name = posixpath.join(
      GCS_ROOT, self.gcs_folder, self.file_name(req, obj))
    gcs_file = cloudstorage.open(file_name, 'w', content_type=img_file.type)
    logging.info('Saving file: %s' % file_name)
    gcs_file.write(img_file.value)
    gcs_file.close()

    setattr(obj, name,
            blobstore.BlobKey(blobstore.create_gs_key('/gs' + file_name)))


class ProfileImageField(ImageField):

  def file_name(self, req, obj):
    return obj.username_lower


class PackshotImageField(ImageField):

  def file_name(self, req, obj):
    return '%s-packshot' % models.slugify(obj.answer_title)


class ScreenshotImageField(ImageField):

  def file_name(self, req, obj):
    return '%s-screenshot' % models.slugify(obj.question.get().answer_title)


class LeagueImageField(ImageField):

  def file_name(self, req, obj):
    return obj.name_slug


class ClueForm(Form):
  """A clue form."""
  text = fields.TextAreaField('Text')
  image = ScreenshotImageField('Image', 'questions')


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


class CurrentUserField(fields.HiddenField):
  """Sets the current user on the entity."""

  def populate_obj(self, entity, name):
    """Populate the current user for the owner field."""
    auth_obj = auth.get_auth()
    user_dict = auth_obj.get_user_by_session()
    entity.owner = ndb.Key('User', user_dict['user_id'])


class LeagueUsersField(fields.HiddenField):
  """Sets the current user on the entity."""

  def process_data(self, user_keys):
    if user_keys:
      user_keys = ','.join([str(key.id()) for key in user_keys])
    super(LeagueUsersField, self).process_data(user_keys)

  def populate_obj(self, entity, name):
    """Populate the users field."""
    if not self.data:
      return
    entity.users = [ndb.Key('User', int(key)) for key in self.data.split(',')]


class OrderedFieldForm(Form):
  """
  Set the order in which the fields populate the model.

  So we can rely on the model having populated fields in subsequent
  populate object calls.
  """

  # The field order list must contain the name of every field.
  field_order = []

  def populate_obj(self, obj):
    """
    Populates the attributes of the passed `obj` with data from the form's
    fields.
    """
    items = sorted(
      self._fields.items(), key=lambda tup: self.field_order.index(tup[0]))

    for name, field in items:
        field.populate_obj(obj, name)


class Question(OrderedFieldForm):

  field_order = [
    'answer',
    'clues',
    'week',
    'season',
    'imdb_url',
    'email_msg',
    'packshot',
  ]

  """A question form."""
  def __init__(self,  **kwargs):
    super(Question, self).__init__( **kwargs)
    self.week.default = WeekField.week_default()
    self.season.choices = SeasonField.season_choices()
  
  answer = FilmField('Film', [validators.Required()], id='film')
  clues = CluesFieldList(ClueFormField(ClueForm), min_entries=4)
  email_msg = fields.TextAreaField('Email Message')
  packshot = PackshotImageField('Image', 'questions')
  imdb_url = fields.TextField('IMDB Link',
                              default='http://www.imdb.com/title/XXX/')
  week = WeekField(choices=WeekField.week_choices())
  season = SeasonField()


class Registration(Form):
  """The registration form."""
  username = fields.TextField('', [validate_username])


class User(OrderedFieldForm):

  field_order = [
    'username',
    'email',
    'favourite_film',
    'pic',
  ]

  username = fields.TextField('', [validate_username])
  email = fields.TextField(validators=[validators.Email()])
  pic = ProfileImageField('pic', 'profiles')
  favourite_film = FilmField()


class League(OrderedFieldForm):

  field_order = [
    'id',
    'name',
    'pic',
    'owner',
    'users',
  ]

  id = fields.HiddenField('')
  name = fields.TextField('', [validate_league_name])
  pic = LeagueImageField('pic', 'leagues')
  owner = CurrentUserField()
  users = LeagueUsersField()

  def users_json(self):
    user_ids = self.users.data
    user_dicts = []
    if user_ids:
      user_ids = user_ids.split(',')
      user_keys = [ndb.Key('User', int(id)) for id in user_ids]
      users = ndb.get_multi(user_keys)
      user_dicts = [user.get_league_user_json() for user in users]
    return json.dumps(user_dicts)
