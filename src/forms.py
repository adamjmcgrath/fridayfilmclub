#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Friday Film Club models."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

from cgi import escape
import datetime
import logging
import re
import posixpath

import webapp2
from google.appengine.api import files
from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.ext.db import BadKeyError
from wtforms import fields, Form, validators, widgets

import models
import settings


_USERNAME_RE = re.compile(r'^[\w\d_]{3,16}$')

class FilmField(fields.HiddenField):
  """A film field."""

  def process_formdata(self, valuelist):
    """Process data received over the wire from a form."""
    try:
      self.data = ndb.Key('Film', valuelist and valuelist[0]).get()
    except BadKeyError:
      self.data = ''

  def populate_obj(self, obj, name):
    """Populate the object represented by the film field."""
    obj.answer = self.data.key


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

    obj.image = files.blobstore.get_blob_key(file_name)


class ClueForm(Form):
  """A clue form."""
  text = fields.TextAreaField('Text')
  image = ImageField('Image')


class ClueFormField(fields.FormField):

  def populate_obj(self, entity):
    """docstring for populate_obj"""

    self.form.populate_obj(entity)


class CluesFieldList(fields.FieldList):
  #
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


class Question(Form):
  """A question form."""
  answer = FilmField('Film', [validators.Required()], id='film')
  clues = CluesFieldList(ClueFormField(ClueForm), min_entries=4)
  email_msg = fields.TextAreaField('Email Message')
  imdb_url = fields.TextField('IMDB Link',
                              default='http://www.imdb.com/title/XXX/')


class Registration(Form):
  """The registration form."""
  invitation_code = fields.TextField()
  username = fields.TextField()

  def validate_username(self, field):
    """Validate the username."""
    username = field.data.strip()
    logging.info(_USERNAME_RE.search(username))
    if not _USERNAME_RE.search(username):
      raise validators.ValidationError('Invalid username.')
    elif models.User.get_by_id(username):
      raise validators.ValidationError('This username is already taken.')

  def validate_invitation_code(self, field):
    """Validate the invite."""
    invitation_code = field.data.strip()
    if not invitation_code:
      raise validators.ValidationError('You need an invitation code.')
    elif not models.Invite.get_by_id(invitation_code):
      raise validators.ValidationError('Not a valid invite.')


class Invite(Form):
  invite_email = fields.TextField(validators=[validators.Email()])