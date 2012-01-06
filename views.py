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
from google.appengine.ext import db

import forms
import models
import settings


VALID_CALLBACK = re.compile('^\w+(\.\w+)*$')



class HomePage(webapp2.RequestHandler):
  """Shows the homepage."""

  def get(self):
    template = settings.jinja_env.get_template('templates/index.html')
    return webapp2.Response(template.render({}))


class Question(webapp2.RequestHandler):
  """Shows the homepage."""

  template_path = 'templates/question.html'

  def get(self, question_key):
    template = settings.jinja_env.get_template(self.template_path)

    if question_key:
      question = models.Question.get(question_key)
    else:
      question = models.Question.all().get()
      question_key = str(question.key())

    user = users.get_current_user()
    user_id = user.user_id()
    user_entity = models.User.get_or_insert(user_id)

    answer_key_name = posixpath.join(user_id, question_key)
    answer = models.Answer.get_or_insert(answer_key_name)
    answer.question = question
    answer.user = user_entity
    answer.put() # TODO(adamjmcgrath) Roll this into get_or_insert?
    form = forms.Answer()

    return webapp2.Response(template.render({
      'answer': answer,
      'dev_mode': settings.is_dev and self.request.get('debugjs'),
      'form': form,
      'question': question,
    }))


  def post(self, question_key):
    template = settings.jinja_env.get_template(self.template_path)

    if question_key:
      question = models.Question.get(question_key)
    else:
      question = models.Question.all().get()
      question_key = str(question.key())

    user = users.get_current_user()
    user_id = user.user_id()
    user_entity = models.User.get_or_insert(user_id)

    answer_key_name = posixpath.join(user_id, question_key)
    answer = models.Answer.get_or_insert(answer_key_name)
    answer.question = question
    answer.user = user_entity
    form = forms.Answer(formdata=self.request.POST)

    if form.validate():
      form.populate_obj(answer)
      answer.put()

    if self.request.get('js'):
      # @TODO(amcgrath) If last guess send correct answer and score.
      json_response = {
        'correct': answer.correct == True,
        'clue': question.clues()[answer.current_guess],
      }
      if answer.incorrect or answer.correct:
        json_response['score'] = answer.score
        json_response['answer'] = question.film.title
      response = json.dumps(json_response)
    else:
      response = template.render({
        'answer': answer,
        'dev_mode': settings.is_dev and self.request.get('debugjs'),
        'form': form,
        'question': question,
      })

    return webapp2.Response(response)
