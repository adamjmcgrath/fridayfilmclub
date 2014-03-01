#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Main views of the Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging
import urlparse
import posixpath

from google.appengine.api import mail, users

import auth
import baserequesthandler
import forms
import models
import twitter

HOST_URL = 'http://www.fridayfilmclub.com'


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
      user=user.key,
      user_is_admin=user.is_admin
    )

    return self.render_template('question.html', {
      'user_question': user_question,
      'question': question,
    })


class Login(baserequesthandler.RequestHandler):
  """Shows the login page."""

  def get(self):
    return self.render_template('login.html', {
      'no_invite_warning': str(self.request.referer).endswith('/login')
    })


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
      # Set the username and invitation in the session and login to the auth provider.
      self.session['username'] = self.request.get('username')
      self.session['invitation_code'] = self.request.get('invitation_code')
      self.redirect(self.uri_for('auth_login', provider=provider))
    else:
      return self.render_template('register.html', {
        'form': form
      })


class RequestInvite(baserequesthandler.RequestHandler):
  """Shows the request invite page."""

  def get(self):
    return self.render_template('requestinvite.html', {
      'form': forms.RequestInvite()
    })

  def post(self):
    form = forms.RequestInvite(self.request.POST)
    sent_to = None
    if form.validate():
      sent_to = form.email.data
      mail.send_mail(sender='fmj@fridayfilmclub.com',
                     to='fmj@fridayfilmclub.com',
                     subject='Invite request',
                     body='Please can I get an invite sent to %s' % sent_to)

      # Reset the form.
      form.process()

    return self.render_template('requestinvite.html', {
      'form': form,
      'sent_to': sent_to
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


class SendInvites(baserequesthandler.RequestHandler):

  @auth.login_required
  def get(self):
    providers = [
      {
        'id': 'google',
        'noun': 'Contacts',
        'has_token': self.current_user.google_refresh_token
      },
      {
        'id': 'facebook',
        'noun': 'Friends',
        'has_token': self.current_user.facebook_uid
      },
      {
        'id': 'twitter',
        'noun': 'Followers',
        'has_token': self.current_user.twitter_token
      },
    ]
    self.session['original_url'] = self.request.url
    return self.render_template('sendinvites.html', {
        'user': self.current_user,
        'providers': providers
    })

  @auth.login_required
  def post(self):

    user = self.current_user
    google_contacts = self.request.get('google-contacts').split(',')
    facebook_contacts = self.request.get('facebook-contacts').split(',')
    twitter_contacts = self.request.get('twitter-contacts').split(',')
    google_sent = []

    for google_contact in google_contacts:
      if google_contact:
        invite = user.invites.pop().id()
        success = send_invite_email(invite, user.google_name,
                                    user.google_email, google_contact)
        if success:
          google_sent.append(google_contact)

    for facebook_contact in facebook_contacts:
      if facebook_contact:
        invite = user.invites.pop().id()
        email = facebook_contact + '@facebook.com'
        success = send_invite_email(invite, user.facebook_name,
                     'fmj@fridayfilmclub.com', email)

    for twitter_contact in twitter_contacts:
      if twitter_contact:
        invite = user.invites.pop().id()
        success = send_invite_dm(invite, user, twitter_contact)

    # user.put()
    return self.render_template('sendinvites.html', {
        'user': self.current_user,
        'fail': not len(google_sent),
        'sent': google_sent,
        'providers': []
    })


class Archive(baserequesthandler.RequestHandler):
  """An archive of old questions."""

  def get(self):
    questions = models.Question.query(models.Question.posed != None,
                                      models.Question.is_current == False)
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


class SendInviteLegacy(baserequesthandler.RequestHandler):
  """Old send invites handler."""

  @auth.login_required
  def post(self):
    user = self.current_user
    form = forms.Invite(self.request.POST)

    if len(user.invites) and form.validate():
      invite = user.invites.pop().id()
      user.put()

      # Send the invite.
      email = form.email.data
      logging.info('Sending invite: %s, to: %s' % (invite, email))
      body = self.generate_template('email/invite.txt', {
        'invite': urlparse.urljoin(self.request.host_url, 'register?invite=%s' % invite),
        'user': user.name
      })
      try:
        sender = user.email
      except AttributeError:
        sender = 'fmj@fridayfilmclub.com'

      try:
        mail.send_mail(sender=sender,
                       to=email,
                       subject='Friday Film Club invitation',
                       body=body)
      except mail.InvalidSenderError:
        mail.send_mail(sender='fmj@fridayfilmclub.com',
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


def send_invite_email(invite, from_name, from_email, to_email):

  # Send the invite.
  logging.info('Sending invite: %s, to: %s' % (invite, to_email))
  template = baserequesthandler.JINJA_ENV.get_template(
        posixpath.join(baserequesthandler.TEMPLATE_PATH, 'email/invite.txt'))
  body = template.render({
    'invite': urlparse.urljoin(HOST_URL, 'register?invite=%s' % invite),
    'user': from_name
  })

  sender = from_email or 'fmj@fridayfilmclub.com'

  try:
    mail.send_mail(sender=sender,
                   to=to_email,
                   subject='Friday Film Club invitation',
                   body=body)
    return True

  except mail.Error:
    return False


def send_invite_dm(invite, from_user, to_handle):

  from_handle = from_user.twitter_name

  logging.info('Sending invite: %s, to: %s' % (invite, to_handle))

  try:
    msg = ('%s has invited you to Friday Film Club: ' +
           'www.fridayfilmclub.com/register?invite=%s')
    twitter.send_dm(from_user, to_handle, msg % (from_handle, invite))
    return True

  except IndexError:
    return False
