#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Friday Film Club models."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

from cgi import escape
import datetime
import logging
import posixpath

import webapp2
from google.appengine.api import files
from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.ext.db import BadKeyError
from wtforms import fields, Form, validators, widgets

import models
import settings



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

  # def validate_text(self, field):
  #   """docstring for validate"""
  #   if ((field.data and self.data['image']) or
  #       (not field.data and not self.data['image'])):
  #     raise validators.ValidationError('Invalid choices.')
  # 
  # def validate_image(self, field):
  #   """docstring for validate"""
  #   if ((field.data and self.data['text']) or
  #       (not field.data and not self.data['text'])):
  #     raise validators.ValidationError('Invalid choices.')


class ClueFormField(fields.FormField):

  def populate_obj(self, entity):
    """docstring for populate_obj"""

    self.form.populate_obj(entity)


class CluesFieldList(fields.FieldList):

  def populate_obj(self, entity, name):
    counter = 0

    for entry, data in zip(self.entries, self.data):
      try:
        clue = entity.clues[counter]
        entry.populate_obj(clue)
        clue.put()
        entity.clues[counter](clue.key)
      except IndexError:
        clue = models.Clue(question=entity.key)
        entry.populate_obj(clue)
        clue.put()
        entity.clues.append(clue.key)
      counter += 1


class Question(Form):
  """A question form."""
  answer = FilmField('Film', [validators.Required()], id='film')
  clues = CluesFieldList(ClueFormField(ClueForm), min_entries=4)
