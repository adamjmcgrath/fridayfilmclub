#!/usr/bin/python
#
# Copyright 2012 Friday Film Club. All Rights Reserved.
"""Authentication."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging

import baserequesthandler
import secrets

import webapp2
from webapp2_extras import auth, sessions

from google.appengine.api import mail
from simpleauth.handler import SimpleAuthHandler

import models
import settings

def login_required(handler_method):
  """A decorator to require that a user be logged in to access a handler.
  """
  def check_login(self, *args, **kwargs):

    if self.logged_in:
      return handler_method(self, *args, **kwargs)
    elif self.request.method == 'POST':
      self.abort(401)
    else:
      self.session['original_url'] = self.request.url
      self.redirect('/login')

  return check_login


class AuthHandler(baserequesthandler.RequestHandler, SimpleAuthHandler):
  """Authentication handler for OAuth 2.0, 1.0(a) and OpenID."""

  USER_ATTRS = {
    'google': {
      'picture': 'pic',
      'name': 'name',
      'link': 'link',
      'email': 'email',
      'refresh_token': 'refresh_token'
    },
    'facebook': {
      'id': lambda id: ('pic', 'http://graph.facebook.com/{0}/picture?type=large'.format(id)),
      'name': 'name',
      'link': 'link',
      'email': 'email',
      'uid': 'uid'
    },
    'twitter': {
      'profile_image_url': lambda url: ('pic', url.replace('_normal','')),
      'screen_name': 'name',
      'link': 'link',
      'token': 'token',
      'token_secret': 'token_secret',
    },
  }

  def _on_signin(self, data, auth_info, provider):
    """Callback whenever a new or existing user is logging in.

    Args:
      data: is a user info dictionary.
      auth_info: contains access token or oauth token and secret.
      provider: the id of the oauth provider.
    """
    auth_id = '%s:%s' % (provider, data['id'])

    if provider == 'facebook':
      data['uid'] = data['id']

    if provider == 'google' and 'refresh_token' in auth_info:
      data['refresh_token'] = auth_info['refresh_token']

    if provider == 'twitter':
      data['token'] = auth_info['oauth_token']
      data['token_secret'] = auth_info['oauth_token_secret']

    logging.info('Looking for a user with id %s' % auth_id)

    user = self.auth.store.user_model.get_by_auth_id(auth_id)

    if user:
      logging.info('Found existing user to log in')
      # existing user. just log them in and update token.
      user.populate(**self._to_user_model_attrs(data, provider, False))
      user.put()
      self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

    else:
      # check whether there is a user currently logged in
      # or that their is a user with this username.

      username = self.session.get('username')

      if self.logged_in:
        logging.info('Updating currently logged in user.')
        u = self.current_user
        u.auth_ids.append(auth_id)
        u.populate(**self._to_user_model_attrs(data, provider, False))
        u.put()
        self.auth.set_session(self.auth.store.user_to_dict(u), remember=True)

      elif username:
        logging.info('Creating a user for %s.' % username)

        # Create a user the given username.
        u = models.User(username=username.strip())

        # Authenticate the new user.
        u.auth_ids.append(auth_id)
        u.populate(**self._to_user_model_attrs(data, provider, True))
        u.put()
        self.auth.set_session(self.auth.store.user_to_dict(u), remember=True)
        del self.session['username']

        # Send registration email.
        try:
          body = self.generate_template('email/registration.txt', {
            'username': username
          })
          mail.send_mail(sender=settings.FMJ_EMAIL,
                         to=u.email,
                         subject='Welcome to Friday Film Club',
                         body=body)
        except:
          logging.info('Failed to send email to %s.' % username)

        self.redirect('/settings')

    # Redirect them to the next page.
    target = self.session.get('original_url')
    if target:
      del self.session['original_url']
      self.redirect(str(target))
    else:
      self.redirect('/settings')

  def logout(self):
    self.auth.unset_session()
    self.redirect('/')

  def _callback_uri_for(self, provider):
    return self.uri_for('auth_callback', provider=provider, _full=True)

  def _get_consumer_info_for(self, provider):
    """Returns a tuple (key, secret) for auth init requests."""
    return secrets.AUTH_CONFIG[provider]

  def _to_user_model_attrs(self, data, provider, new_user):
    attrs_map = self.USER_ATTRS[provider]
    user_attrs = {}
    for k, v in data.iteritems():
      if k in attrs_map:
        if isinstance(attrs_map[k], str):
          key = attrs_map[k]
          value = v
        else:
          values = attrs_map[k](v)
          key = values[0]
          value = values[1]
        provider_key = '%s_%s' % (provider, key)
        user_attrs.setdefault(provider_key, value)

        if new_user:
          if key == 'pic':
            value = models.User.blob_from_url(value)
          user_attrs.setdefault(key, value)

    return user_attrs
