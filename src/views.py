#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Main views of the Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging
from operator import itemgetter
import uuid

from google.appengine.api import channel, files, users
from google.appengine.ext import ndb

import auth
import baserequesthandler
import forms
import models
import settings

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

  def get(self, question_id):

    if question_id:
      question = models.Question.get_by_id(int(question_id))
    else:
      question = models.Question.query(models.Question.is_current == True).get()

    logged_in = self.logged_in

    # Only admins can view a question before it's posed,
    # only logged in users can view the current question.
    if ((not question.posed and not users.is_current_user_admin()) or
       (question.is_current and not logged_in)):
      self.session['original_url'] = self.request.url
      return self.redirect('/login')

    if logged_in:
      user = self.current_user
    else:
      user = models.AnonymousUser.get(
        existing_user_id=self.session.get('anonymous_user'))
      user_key = user.put()
      self.session['anonymous_user'] = user_key.id()

    user_question_id = '%d-%s' % (question.key.id(), user.key.id())
    user_question = models.UserQuestion.get_or_insert(
        user_question_id,
        question=question.key,
        user=user.key,
        user_is_admin=user.is_admin,
        user_is_anonymous=bool(user.is_anonymous)
    )

    context = {
      'user': user,
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
      # Set the username and invitation in the session and login to the
      # auth provider.
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

  def get(self, league=None):
    if league:
      league = models.League.get_by_name(league)
    self.render_template('leaderboard.html', {
      'channel_token': channel.create_channel(str(uuid.uuid4())),
      'league': league,
      'season': models.Season.get_current()
    })


class HighScores(baserequesthandler.RequestHandler):
  """The high scores page."""

  def get(self, league=None):
    user_question_query = models.UserQuestion.query().order(
        -models.UserQuestion.score)

    if league:
      league = models.League.get_by_name(league)
      user_question_query = user_question_query.filter(
          models.UserQuestion.user.IN(league.users))

    self.render_template('highscores.html', {
      'user_questions': user_question_query.fetch(10),
      'league': league
    })


class HowItWorks(baserequesthandler.RequestHandler):
  """How it works / rules."""

  def get(self):
    self.render_template('how.html', {})


class AddEditLeague(baserequesthandler.RequestHandler):
  """Add / Edit leagues."""

  @auth.login_required
  def get(self, league=None):

    owner_key = self.current_user.key
    if league:
      league = models.League.get_by_id(int(league))
      owner_key = league.owner

    user_keys = league.users if league else []

    if owner_key in user_keys:
      user_keys.remove(owner_key)

    self.render_template('addeditleague.html', {
      'league_name': league.name if league else '',
      'league_pic': league.pic_url() if league else '',
      'users': ndb.get_multi(user_keys) if league else [],
      'to_json': models.User.to_league_users_json
    })

  @auth.login_required
  def post(self, league=None):

    owner_key = self.current_user.key
    if league:
      league = models.League.get_by_id(int(league))
      owner_key = league.owner

    post_dict = self.request.POST
    errors = {}
    user_keys = []
    pic = None
    league_name = league.name if league else ''

    if post_dict['name']:
      if models.League.get_by_name(models.slugify(post_dict['name'])):
        errors['name'] = 'League name already exists.'
      league_name = post_dict['name']
    else:
      errors['name'] = 'No league name specified.'

    if post_dict['users']:
      user_key_names = post_dict['users'].split(',')
      user_keys = [ndb.Key('User', int(key)) for key in user_key_names]
    elif league:
      user_keys = list(league.users)

    if post_dict['pic']:
      img_file = self.request.get('pic')
      file_name = files.blobstore.create(mime_type='application/octet-stream')
      with files.open(file_name, 'a') as f:
        f.write(img_file)
      files.finalize(file_name)
      pic = files.blobstore.get_blob_key(file_name)

    if owner_key in user_keys:
      user_keys.remove(owner_key)

    if not len(errors.keys()):
      if league:
        league.name = league_name
        league.pic = pic or league.pic
        league.put()
        league.add_users(
          ndb.get_multi(list(set(user_keys) - set(league.users))))
        league.remove_users(
          ndb.get_multi(list(set(league.users) - set(user_keys))))
      else:
        league = models.League.create(
          self.current_user,
          league_name,
          users=ndb.get_multi(user_keys),
          pic=pic)
        league.put()

    if len(errors.keys()) == 0:
      return self.redirect(
        self.uri_for('leader-board-league', league=league.name_slug))
    else:
      self.render_template('addeditleague.html', {
        'league_name': league_name,
        'league_pic': league and league.pic_url(),
        'users': ndb.get_multi(user_keys),
        'errors': errors,
        'to_json': models.User.to_league_users_json
      })
