#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.
"""Handles the Movie Auto Complete UI."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import datetime
import logging
import urlparse

import webapp2
from google.appengine.api import memcache, taskqueue, users, mail
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import blobstore, ndb
from google.appengine.ext.webapp import blobstore_handlers

from mapreduce import control, mapreduce_pipeline
from mapreduce.model import MapreduceState

import baserequesthandler
import forms
import map_reduce
import models

EMAIL_BATCH_SIZE = 10


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
      return webapp2.redirect('/admin')
    else:
      return self.render_template('admin/addquestion.html', {
          'form': form,
          'question': question_entity,
          'debug': self.request.get('debug')
      })



class Questions(baserequesthandler.RequestHandler):
  """Adds a question to the datastore."""

  def get(self):
    questions = models.Question.query().order(
      models.Question.season, models.Question.week)

    return self.render_template('admin/questions.html', {
      'questions': questions
    })


class PoseQuestion(baserequesthandler.RequestHandler):
  """Email the question out to the users and post it on the twitter/FB feed."""

  def get(self):
    """Create a queue for sending out the emails. Triggered weekly by a cron."""
    if not self.request.headers.get('X-Appengine-Cron'):
      return self.error(403)

    prev_question = models.Question.get_current()
    next_question = models.Question.get_next()
    now = datetime.datetime.now()

    if not (prev_question and next_question):
      return logging.error('There is no next question to pose.')

    last_posed_delta = now - prev_question.posed
    if last_posed_delta.days < 6:
      return logging.error('The last question was posed less than a week ago.')

    prev_question.is_current = False
    next_question.is_current = True
    next_question.posed = now
    ndb.put_multi([prev_question, next_question])

    subject = ('Friday Film Club: Season %s, Week %d' %
               (next_question.season.id(), next_question.week))
    taskqueue.add(url=self.request.path,
                  params={
                    'msg': next_question.email_msg,
                    'subject': subject,
                    'question': next_question.key.id()
                  },
                  queue_name='pose')

    logging.info('Question: %s, posed', next_question.answer.id())

  def post(self):
    """Queue handler for sending out each email."""
    cursor = self.request.get('cursor') or None
    if cursor:
      cursor = Cursor(urlsafe=cursor)
    q = models.User.query()
    user_entities, next_cursor, more = q.fetch_page(EMAIL_BATCH_SIZE,
                                                    start_cursor=cursor)
    subject = self.request.get('subject')
    msg = self.request.get('msg')
    question = self.request.get('question')

    body = self.generate_template('email/question.txt', {
      'url': urlparse.urljoin(self.request.host_url, 'question/%s' % question),
      'msg': msg
    })

    for user_entity in user_entities:
      mail.send_mail(sender='fmj@fridayfilmclub.com',
                     to=user_entity.email,
                     subject=subject,
                     body=body)

    if more:
      taskqueue.add(url=self.request.path,
                    params={
                      'msg': msg,
                      'subject': subject,
                      'question': question,
                      'cursor': next_cursor.urlsafe()
                    },
                    queue_name='pose')


class PoseQuestionTest(baserequesthandler.RequestHandler):

  def get(self, key):
    """Sends a test email to the admins."""
    question = models.Question.get_by_id(int(key))

    body = self.generate_template('email/question.txt', {
      'url': urlparse.urljoin(self.request.host_url,
                              'question/%s' % key),
      'msg': question.email_msg,
      'name': 'Admin'
    })

    mail.send_mail(sender='fmj@fridayfilmclub.com',
                   to=users.get_current_user().email(),
                   subject='Friday Film Club TEST',
                   body=body)

    self.redirect(self.uri_for('admin-homepage'))


class SendInvites(baserequesthandler.RequestHandler):
  """Send invites to users from admin section"""

  def get(self):
    return self.render_template('admin/sendinvites.html', {
      'form': forms.Invite()
    })

  def post(self):
    form = forms.Invite(self.request.POST)
    sent_to = False
    if form.validate():
      # Send invite
      email = form.invite_email.data
      invite = models.Invite.create_single_invite().id()
      logging.info('Sending invite: %s, to: %s' % (invite, email))
      body = self.generate_template('email/invite.txt', {
        'invite': urlparse.urljoin(self.request.host_url, 'register?invite=%s' % invite),
        'user': 'Film Master Jack'
      })
      mail.send_mail(sender='fmj@fridayfilmclub.com',
                       to=email,
                       subject='Friday Film Club invitation',
                       body=body)
      form = forms.Invite()
      sent_to = email

    return self.render_template('admin/sendinvites.html', {
      'form': form,
      'sent_to': sent_to
    })


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
