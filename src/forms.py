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
from google.appengine.ext.db import BadKeyError
from wtforms import fields, Form, validators, widgets

import models
import settings



class FilmWidget(object):
  """Renders a film input.
  
  <input type="text" autocomplete="off" value="Top Gun"
         name="film" id="film">
  <input id="film_key" type="hidden" value="xyz_123">
  """

  def __call__(self, field, **kwargs):
    kwargs.setdefault('id', field.id)
    
    html_string = (u'<input type="text" autocomplete="off" value="%s" id="ac">'
                    '<input id="film" type="hidden" value="%s" %s>')
    film_entity = field.data

    params = widgets.html_params(name=field.name, **kwargs)
    value = field.data and escape(unicode(field.data.title)) or u''
    key_value = field.data and unicode(field.data.key()) or u''
    return widgets.HTMLString(html_string %
        (value, key_value, params))


class GuessWidget(object):
  """Renders a film input.
  
  <input type="text" autocomplete="off" value="Top Gun"
         name="film" id="film">
  <input id="film_key" type="hidden" value="xyz_123">
  """

  def __call__(self, field, **kwargs):
    kwargs.setdefault('id', field.id)
    
    html_string = (u'<input type="text" autocomplete="off" id="ac">'
                    '<input id="film" type="hidden" %s>')
    film_entity = field.data

    params = widgets.html_params(name=field.name, **kwargs)
    return widgets.HTMLString(html_string % params)


class FilmField(fields.TextField):
  """A film field."""
  widget = FilmWidget()

  def process_formdata(self, valuelist):
    """Process data received over the wire from a form."""
    try:
      self.data = models.Film.get(valuelist and valuelist[0])
    except BadKeyError:
      self.data = ''

  def populate_obj(self, obj, name):
    """Populate the object represented by the film field."""
    obj.film = self.data.key()


class ScreenShotField(fields.FileField):
  """A clue field."""

  def populate_obj(self, obj, name):
    """Populate the object represented by the film field."""
    req = webapp2.get_request()
    img_file = req.get(name)
    if not img_file:
      return
    file_name = files.blobstore.create(mime_type='application/octet-stream')
    with files.open(file_name, 'a') as f:
      f.write(img_file)
    files.finalize(file_name)
    obj.screenshot = files.blobstore.get_blob_key(file_name)


class GuessField(FilmField):
  """A guess field."""
  widget = GuessWidget()

  def populate_obj(self, obj, name):
    """Populate the object represented by the film field."""
    if obj.correct or obj.incorrect:
      return

    correct = (self.data.key() == obj.question.film.key())
    setattr(obj, ('guess_%d' % obj.current_guess), str(self.data.key()))

    if correct:
      obj.correct = True
      obj.answered_correctly = datetime.datetime.now()
      obj.score = obj.calculate_score()
    elif (obj.current_guess == 3) and not correct:
      obj.incorrect = True
      obj.score = 0
    else:
      obj.current_guess += 1


class Question(Form):
  """A question form."""
  film = FilmField(id='film')
  screenshot = ScreenShotField('Screenshot')
  clue_1 = fields.TextAreaField('Clue 1')
  clue_2 = fields.TextAreaField('Clue 2')
  clue_3 = fields.TextAreaField('Clue 3')


class Answer(Form):
  """An answer form."""
  guess = GuessField('Guess', [validators.Required()])
