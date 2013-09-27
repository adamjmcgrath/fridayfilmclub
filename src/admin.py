#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.
"""Handles the Movie Auto Complete UI."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

from datetime import datetime
import logging
import os
import re
import urlparse

import webapp2
from google.appengine.api import memcache, taskqueue, users, mail
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

from mapreduce import control, mapreduce_pipeline
from mapreduce.model import MapreduceState

import baserequesthandler
import forms
import map_reduce
import models
import settings



class HomePage(baserequesthandler.RequestHandler):
  """Shows the homepage."""

  def get(self):
    return self.render_template('admin/index.html', {})


class AddFilms(baserequesthandler.RequestHandler):
  """Form for uploading films as a CSV file as '{Year}, {Title}'."""

  def get(self):
    upload_url = blobstore.create_upload_url('/admin/addfilmshandler')

    return self.render_template('admin/addfilms.html', {
        'upload_url': upload_url
    })


class AddEditQuestion(baserequesthandler.RequestHandler):
  """Adds a question to the datastore."""

  def get(self, key=None):
    if key:
      question_entity = ndb.Key('Question', int(key)).get()

      form = forms.Question(obj=question_entity)
    else:
      question_entity = None
      form = forms.Question()
    
    return self.render_template('admin/addquestion.html', {
        'form': form,
        'question': question_entity,
    })

  def post(self, key=None):
    if key:
      question_entity = ndb.Key('Question', int(key)).get()
    else:
      question_entity = models.Question()

    form = forms.Question(formdata=self.request.POST, obj=question_entity)

    if form.validate():
      # TODO(adamjmcgrath): only put once.
      question_entity.put()
      form.populate_obj(question_entity)
      question_entity.put()
      return webapp2.redirect('/admin/questions')
    else:
      return self.render_template('admin/addquestion.html', {
          'form': form,
          'question': question_entity,
          'debug': self.request.get('debug')
      })



class Questions(baserequesthandler.RequestHandler):
  """Adds a question to the datastore."""

  def get(self):
    return self.render_template('admin/questions.html', {
      'questions': models.Question.query(),
    })


class PoseQuestion(baserequesthandler.RequestHandler):
  """Email the question out to the users and post it on the twitter/FB feed."""

  def get(self, key):
    """Create a queue for sending out the emails."""
    debug = self.request.get('debug')
    user_entities = models.User.query()
    old_question = models.Question.query(
                       models.Question.is_current == True).get()
    if old_question:
      old_question.is_current = False
      old_question.put()

    question = models.Question.get_by_id(int(key))
    now = datetime.now()
    url = self.request.path

    if question.posed and not debug:
      return self.response.out.write('You\'ve already posed this question.')

    if not debug:
      question.posed = now
      question.is_current = True
      question.put()

    if (debug):
      taskqueue.add(url=self.request.path,
                    params={'email': users.get_current_user().email()},
                    queue_name='pose')
    else:
      # TODO (adamjmcgrath) Batch the loop through users.
      for user_entity in user_entities:
        taskqueue.add(url=url,
                      params={'email': user_entity.email},
                      queue_name='pose')

    logging.info('Question: %s, posed at: %s', question.answer.id(),
        now.strftime('%H:%M.%s on %d/%M/%Y'))

    return self.render_template('admin/posed.html', {
      'all_users': not debug,
      'question': question,
      'url': url
    })

  def post(self, key):
    """Queue handler for sending out each email."""
    email = self.request.get('email')
    link = urlparse.urljoin(self.request.host_url, 'question/%s' % key)
    mail.send_mail(sender='adamjmcgrath@gmail.com',
                     to=email,
                     subject='This weeks Friday Film Club question',
                     body='Go play: %s' % link)


class AddFilmsHandler(blobstore_handlers.BlobstoreUploadHandler):
  """Processes the uploaded films and creates a blob to upload and index."""

  def post(self):
    upload_files = self.get_uploads('file')
    blob_info = upload_files[0]

    batch = 1
    last_add = models.Film.query().order(-models.Film.batch).get()
    if last_add:
      batch += last_add.batch

    logging.info('Uploading film batch: %d.' % batch)

    mapreduce_parameters = {
      'blob_key': str(blob_info.key()),
      'done_callback': '/admin/addfilmsdone',
    }
    
    mapper_parameters = {
      'blob_keys': str(blob_info.key()),
      'batch': batch
    }

    map_reduce_id = control.start_map(
        'Add films to datastore.', # Name
        'map_reduce.add_film_map', # handler_spec
        'mapreduce.input_readers.BlobstoreLineInputReader', # reader_spec
        mapper_parameters, # mapper_parameters
        mapreduce_parameters=mapreduce_parameters)

    return webapp2.redirect('/admin')


class AddFilmsDone(baserequesthandler.RequestHandler):
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


class IndexFilms(baserequesthandler.RequestHandler):
  """Index's the films."""

  def post(self):
    logging.info('Start indexing films.')
    pipeline = map_reduce.IndexerPipeline()
    pipeline.start()

    return webapp2.redirect('/admin')
