#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Main views of the Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging


from google.appengine.api import users

import auth
import baserequesthandler
import models



class HomePage(baserequesthandler.RequestHandler):
  """Shows the homepage."""

  def get(self):
    current_question = models.Question.query(models.Question.is_current == True)
    question_image = current_question.get().clue_image_url(size=260)
    return self.render_template('index.html', {
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
      user=user.key
    )

    return self.render_template('question.html', {
      'user_question': user_question,
      'question': question,
    })


class Login(baserequesthandler.RequestHandler):
  """Shows the login page."""

  def get(self):
    return self.render_template('login.html', {})


class Settings(baserequesthandler.RequestHandler):
  """Shows the Settings page."""

  @auth.login_required
  def get(self):
    return self.render_template('settings.html', {})


class Archive(baserequesthandler.RequestHandler):
  """An archive of old questions."""

  def get(self):
    return self.render_template('archive.html', {})


class LeaderBoard(baserequesthandler.RequestHandler):
  """The leader board / results page."""

  def get(self):
    return self.render_template('leaderboard.html', {
      'season': models.Season.get_current()
    })


class HowItWorks(baserequesthandler.RequestHandler):
  """How it works / rules."""

  def get(self):
    return self.render_template('how.html', {})
