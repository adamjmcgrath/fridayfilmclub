#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Main views of the Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging
import urlparse
from operator import itemgetter
import posixpath
import uuid

from google.appengine.api import channel, mail, users
from google.appengine.ext import ndb

import auth
import baserequesthandler
import forms
import models
import settings
import twitter

HOST_URL = 'http://www.fridayfilmclub.com'


class HomePage(baserequesthandler.RequestHandler):
  """Shows the homepage."""

  def get(self):
    current_question = models.Question.query(models.Question.is_current == True)
    q = current_question.get()
    question_image = q and q.clue_image_url(size=260)
    self.render_template('index.html', {
        'current_question': current_question,
        'question_image': question_image
    })


class Question(baserequesthandler.RequestHandler):
  """Shows the homepage."""

  @auth.login_required
  def get(self, question_id):

    if question_id:
      question = models.Question.get_by_id(int(question_id))
    else:
      question = models.Question.query(models.Question.is_current == True).get()

    # Only Admins can view a question before it's posed
    if not question.posed and not users.is_current_user_admin():
      return self.error(401)

    user = self.current_user

    user_question_id = '%d-%s' % (question.key.id(), user.key.id())
    user_question = models.UserQuestion.get_or_insert(user_question_id,
      question=question.key,
      user=user.key,
      user_is_admin=user.is_admin
    )

    context = {
      'user_question': user_question,
      'question': question,
    }
    if question.is_current or settings.DEBUG:
      # Add the realtime scores token.
      context['channel_token'] = channel.create_channel(user_question_id)

    self.render_template('question.html', context)


class Login(baserequesthandler.RequestHandler):
  """Shows the login page."""

  def get(self):
    self.render_template('login.html', {})


class Register(baserequesthandler.RequestHandler):
  """Shows the registration page."""

  def get(self):
    form = forms.Registration()
    self.render_template('register.html', {
      'form': form
    })

  def post(self):
    provider = self.request.get('provider')
    form = forms.Registration(self.request.POST)
    if form.validate():
      # Set the username and invitation in the session and login to the auth provider.
      self.session['username'] = self.request.get('username')
      self.redirect(self.uri_for('auth_login', provider=provider))
    else:
      self.render_template('register.html', {
        'form': form
      })


class Profile(baserequesthandler.RequestHandler):
  "The user profile page"

  def get(self, username):
    user = models.User.get_by_username(username)
    user_questions = models.UserQuestion.query(
        models.UserQuestion.user == user.key).map(
          models.UserQuestion.get_profile_dict)

    if not user:
      self.error(404)
    else:
      self.render_template('profile.html', {
        'user_profile': user,
        'user_questions': sorted(user_questions,
                                 key=itemgetter('season', 'week'))
      })


class Settings(baserequesthandler.RequestHandler):
  """Shows the Settings page."""

  @auth.login_required
  def get(self):
    user = self.current_user
    self.render_template('settings.html', {
      'form': forms.User(obj=user, username=user.key.id())
    })

  @auth.login_required
  def post(self):
    user = self.current_user
    form = forms.User(formdata=self.request.POST)
    success = False
    if form.validate():
      form.populate_obj(user)
      user.put()
      success = True
    self.render_template('settings.html', {
      'form': form,
      'success': success
    })


class Archive(baserequesthandler.RequestHandler):
  """An archive of old questions."""

  def get(self):
    questions = models.Question.query(models.Question.posed != None,
                                      models.Question.is_current == False)
    self.render_template('archive.html', {
      'questions': questions
    })


class LeaderBoard(baserequesthandler.RequestHandler):
  """The leader board / results page."""

  def get(self):
    self.render_template('leaderboard.html', {
      'channel_token': channel.create_channel(str(uuid.uuid4())),
      'season': models.Season.get_current()
    })


class HighScores(baserequesthandler.RequestHandler):
  """The leader board / results page."""

  def get(self):
    user_questions = models.UserQuestion.query().order(
        -models.UserQuestion.score).fetch(10)
    self.render_template('highscores.html', {
      'user_questions': user_questions
    })


class HowItWorks(baserequesthandler.RequestHandler):
  """How it works / rules."""

  def get(self):
    self.render_template('how.html', {})
