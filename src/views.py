#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Main views of the Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging
import urlparse


from google.appengine.api import mail, users

import auth
import baserequesthandler
import forms
import models



class HomePage(baserequesthandler.RequestHandler):
  """Shows the homepage."""

  def get(self):
    current_question = models.Question.query(models.Question.is_current == True)
    q = current_question.get()
    question_image = q and q.clue_image_url(size=260)
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


class Register(baserequesthandler.RequestHandler):
  """Shows the registration page."""

  def get(self):
    form = forms.Registration(invitation_code=self.request.get('invite'))
    return self.render_template('register.html', {
      'form': form
    })

  def post(self):
    provider = self.request.get('provider')
    form = forms.Registration(self.request.POST)
    if form.validate():
      # Create a user the given username and delete the invite.
      username = self.request.get('username')
      invitation_code = self.request.get('invitation_code')
      user = models.User(username=username, invites=models.Invite.create_invites(username))
      invite = models.Invite.get_by_id(invitation_code)
      user.put()
      invite.key.delete()

      # Set the username in the session and login to the auth provider.
      self.session['username'] = username
      self.redirect(self.uri_for('auth_login', provider=provider))
    else:
      return self.render_template('register.html', {
        'form': form
      })


class Profile(baserequesthandler.RequestHandler):
  "The user profile page"

  def get(self, username):
    user = models.User.get_by_username(username)
    if not user:
      return self.error(404)
    else:
      return self.render_template('profile.html', {
        'user_profile': user,
        'user_questions': models.UserQuestion.query(models.UserQuestion.user == user.key)
      })



class Settings(baserequesthandler.RequestHandler):
  """Shows the Settings page."""

  @auth.login_required
  def get(self):
    user = self.current_user
    return self.render_template('settings.html', {
      'form': forms.User(obj=user, username=user.key.id())
    })

  @auth.login_required
  def post(self):
    user = self.current_user
    form = forms.User(formdata=self.request.POST)
    if form.validate():
      form.populate_obj(user)
      user.put()
    return self.render_template('settings.html', {
      'form': form
    })


class SendInvite(baserequesthandler.RequestHandler):

  @auth.login_required
  def post(self):
    user = self.current_user
    form = forms.Invite(self.request.POST)

    if len(user.invites) and form.validate():
      invite = user.invites.pop().id()
      user.put()

      # Send the invite.
      email = form.invite_email.data
      logging.info('Sending invite: %s, to: %s' % (invite, email))
      body = self.generate_template('email/invite.txt', {
        'invite': urlparse.urljoin(self.request.host_url, 'register?invite=%s' % invite),
        'user': user.key.id()
      })
      mail.send_mail(sender='adamjmcgrath@gmail.com',
                       to=email,
                       subject='Friday Film Club invitation',
                       body=body)

      return self.render_json({
        'success': True,
        'invites': len(user.invites)
      })

    else:
      if form.invite_email.errors:
        error = form.invite_email.errors[0]
      else:
        error = 'You have no invites left.'

      return self.render_json({
        'success': False,
        'error': error
      })


class Archive(baserequesthandler.RequestHandler):
  """An archive of old questions."""

  def get(self):
    questions = models.Question.query(models.Question.posed != None, models.Question.is_current == False)
    return self.render_template('archive.html', {
      'questions': questions
    })


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
