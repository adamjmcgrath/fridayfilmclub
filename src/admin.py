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
from google.appengine.ext import ndb

import baserequesthandler
import forms
import models
import settings

EMAIL_BATCH_SIZE = 10

def get_question_url(host_url, question_key):
    # Make sure the live cron job doesn't use the appspot.com url.
    if 'appspot.com' in host_url:
      url = 'http://www.fridayfilmclub.com'
    else:
      url = host_url

    return urlparse.urljoin(url, 'question/%s' % question_key)


class HomePage(baserequesthandler.RequestHandler):
  """Shows the homepage."""

  def get(self):
    self.render_template('admin/index.html', {})


class AddEditQuestion(baserequesthandler.RequestHandler):
  """Adds a question to the datastore."""

  def get(self, key=None):
    if key:
      question_entity = ndb.Key('Question', int(key)).get()

      form = forms.Question(obj=question_entity)
    else:
      question_entity = None
      form = forms.Question()

    self.render_template('admin/addquestion.html', {
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
      webapp2.redirect('/admin')
    else:
      self.render_template('admin/addquestion.html', {
          'form': form,
          'question': question_entity,
          'debug': self.request.get('debug')
      })


class Questions(baserequesthandler.RequestHandler):
  """Adds a question to the datastore."""

  def get(self):
    questions = models.Question.query(models.Question.season != None).order(
      models.Question.season, models.Question.week)

    self.render_template('admin/questions.html', {
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

    logging.info('Question: %s, posed', next_question.answer_title)

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
      'url': get_question_url(self.request.host_url, question),
      'msg': msg
    })

    for user_entity in user_entities:
      try:
        email = user_entity.email
      except AttributeError:
        continue

      mail.send_mail(sender=settings.FMJ_EMAIL,
                     to=email,
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
      'url': get_question_url(self.request.host_url, key),
      'msg': question.email_msg,
      'name': 'Admin'
    })

    mail.send_mail(sender=settings.FMJ_EMAIL,
                   to=users.get_current_user().email(),
                   subject='Friday Film Club TEST',
                   body=body)

    self.redirect(self.uri_for('admin-homepage'))


class DryRun(baserequesthandler.RequestHandler):

  def get(self):
    """Sends a test email to the admins."""
    key = self.request.get('key')
    if key:
      question = models.Question.get_by_id(int(key))
    else:
      question = models.Question.get_next()

    if question and not len(question.errors()):
      email_body = self.generate_template('email/question.txt', {
        'url': get_question_url(self.request.host_url, question.key.id()),
        'msg': question.email_msg,
        'name': 'Admin'
      })
      subject = ('Friday Film Club: Season %s, Week %d (DRY RUN)' %
                 (question.season.id(), question.week))
    else:
      email_body = self.generate_template('email/dryrun.txt',
                                          {'question': question})
      subject = 'Friday Film Club (FAILURE)'

    mail.send_mail_to_admins(settings.FMJ_EMAIL, subject, email_body)

    self.response.headers['content-type'] = 'text/plain'
    self.response.out.write(email_body)


class SendInvites(baserequesthandler.RequestHandler):
  """Send invites to users from admin section"""

  def get(self):
    self.render_template('admin/sendinvites.html', {
      'form': forms.Invite()
    })

  def post(self):
    form = forms.Invite(self.request.POST)
    sent_to = False
    if form.validate():
      # Send invite
      email = form.email.data
      invite = models.Invite.create_single_invite().id()
      logging.info('Sending invite: %s, to: %s' % (invite, email))
      body = self.generate_template('email/invite.txt', {
        'invite': urlparse.urljoin(self.request.host_url, 'register?invite=%s' % invite),
        'user': 'Film Master Jack'
      })
      mail.send_mail(sender=settings.FMJ_EMAIL,
                       to=email,
                       subject='Friday Film Club invitation',
                       body=body)
      form = forms.Invite()
      sent_to = email

    self.render_template('admin/sendinvites.html', {
      'form': form,
      'sent_to': sent_to
    })
