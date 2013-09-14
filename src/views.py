#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Main views of the Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import json
import logging
import os
import posixpath
import re

import webapp2
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import ndb

import auth
import baserequesthandler
import forms
import models
import settings



class HomePage(baserequesthandler.RequestHandler):
  """Shows the homepage."""

  def get(self):
    return self.render_template('index.html', {})


class Question(baserequesthandler.RequestHandler):
  """Shows the homepage."""

  @auth.login_required
  def get(self, question_id):

    if question_id:
      question = models.Question.get_by_id(int(question_id))
    else:
      question = models.Question.query().get()

    user = self.current_user

    user_question_id = '%d-%s' % (question.key.id(), user.key.id())
    user_question = models.UserQuestion.get_or_insert(user_question_id,
      question=question.key,
      user=user.key
    )

    return self.render_template('question.html', {
      'user_question': user_question,
      'question': question,
    })


class Login(baserequesthandler.RequestHandler):
  """Shows the profile page."""

  def get(self):
    return self.render_template('login.html', {})


class Profile(baserequesthandler.RequestHandler):
  """Shows the profile page."""

  @auth.login_required
  def get(self):
    return self.render_template('profile.html', {})
