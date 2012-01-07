#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.
"""Handles the Movie Auto Complete UI."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging
import os
import re

import webapp2
from google.appengine.api import memcache
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext.webapp import blobstore_handlers

from mapreduce import control, mapreduce_pipeline
from mapreduce.model import MapreduceState

import forms
import map_reduce
import models
import settings

VALID_CALLBACK = re.compile('^\w+(\.\w+)*$')



class HomePage(webapp2.RequestHandler):
  """Shows the homepage."""

  def get(self):
    template = settings.jinja_env.get_template(
        'templates/admin/index.html')
    return webapp2.Response(template.render({}))


class AddFilms(webapp2.RequestHandler):
  """Form for uploading films as a CSV file as '{Year}, {Title}'."""

  def get(self): 
    template = settings.jinja_env.get_template('templates/admin/addfilms.html')
    upload_url = blobstore.create_upload_url('/admin/addfilmshandler')
    return webapp2.Response(template.render({
      'upload_url': upload_url
    }))


class AddEditQuestion(webapp2.RequestHandler):
  """Adds a question to the datastore."""

  def get(self, key=None):
    if key:
      question_entity = models.Question.get(key)

      form = forms.Question(obj=question_entity)
    else:
      question_entity = None
      form = forms.Question()
    
    template = settings.jinja_env.get_template(
        'templates/admin/addquestion.html')
    return webapp2.Response(template.render({
      'form': form,
      'question': question_entity,
      'dev_mode': settings.is_dev and self.request.get('debugjs')
    }))

  def post(self, key=None):
    form = forms.Question(formdata=self.request.POST)
    template = settings.jinja_env.get_template(
        'templates/admin/addquestion.html')

    if key:
      question_entity = models.Question.get(key)
    else:
      question_entity = models.Question()

    form.populate_obj(question_entity)
    if form.validate():
      question_entity.put()
      return webapp2.redirect('/admin/questions')
    else:
      return webapp2.Response(template.render({
      'form': form,
      'film_entity': film_title,
      'dev_mode': settings.is_dev and self.request.get('debugjs')
    }))


class Questions(webapp2.RequestHandler):
  """Adds a question to the datastore."""

  def get(self):
    template = settings.jinja_env.get_template('templates/admin/questions.html')
    return webapp2.Response(template.render({
      'questions': models.Question.all(),
    }))


class AddFilmsHandler(blobstore_handlers.BlobstoreUploadHandler):
  """Processes the uploaded films and create's a blob to upoad and index."""

  def post(self):
    upload_files = self.get_uploads('file')
    blob_info = upload_files[0]

    mapreduce_parameters = {
      'blob_key': str(blob_info.key()),
      'done_callback': '/admin/addfilmsdone',
    }

    map_reduce_id = control.start_map(
        'Add films to datastore.', # Name
        'map_reduce.add_film_map', # handler_spec
        'mapreduce.input_readers.BlobstoreLineInputReader', # reader_spec
        {'blob_keys': str(blob_info.key())}, # mapper_parameters
        mapreduce_parameters=mapreduce_parameters)

    return webapp2.redirect('/admin')


class AddFilmsDone(webapp2.RequestHandler):
  """Delete the blob once the films have been added to the datastore."""

  def post(self):
    logging.info('Add Movies Complete.')
    mr_id = self.request.headers['Mapreduce-Id']
    mr_state = MapreduceState.get_by_key_name(mr_id)
    mr_spec = mr_state.mapreduce_spec
    json_spec = mr_spec.to_json()
    json_params = json_spec['params']
    blob_key = json_params['blob_key']
    blob_info = blobstore.BlobInfo.get(blob_key)
    blob_info.delete()
    logging.info('Temp blob deleted for mapreduce: %s' % mr_id)


class IndexFilms(webapp2.RequestHandler):
  """Index's the films."""

  def post(self):
    logging.info('Start indexing films.')
    pipeline = map_reduce.IndexerPipeline()
    pipeline.start()

    return webapp2.redirect('/admin')