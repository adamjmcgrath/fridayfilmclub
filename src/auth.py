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

from simpleauth.handler import SimpleAuthHandler


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
    'google'   : {
      'picture': 'avatar_url',
      'name'   : 'name',
      'link'   : 'link',
      'email'   : 'email',
    },
    'facebook' : {
      'id': lambda id: ('avatar_url', 'http://graph.facebook.com/{0}/picture?type=large'.format(id)),
      'name'   : 'name',
      'link'   : 'link',
      'email'   : 'email',
    },
    'twitter'  : {
      'profile_image_url': lambda url: ('avatar_url', url.replace('_normal','')),
      'screen_name'      : 'name',
      'link'             : 'link',
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
    logging.info('Looking for a user with id %s' % auth_id)
    logging.info(data)

    user = self.auth.store.user_model.get_by_auth_id(auth_id)
    if user:
      logging.info('Found existing user to log in')
      # existing user. just log them in.
      self.auth.set_session(self.auth.store.user_to_dict(user))

    else:
      # check whether there's a user currently logged in
      # then, create a new user if nobody's signed in, 
      # otherwise add this auth_id to currently logged in user.
      if self.logged_in:
        logging.info('Updating currently logged in user')
        u = self.current_user
        u.auth_ids.append(auth_id)
        u.populate(**self._to_user_model_attrs(data, provider))
        u.put()

      else:
        logging.info('Creating a brand new user')
        ok, user = self.auth.store.user_model.create_user(
            auth_id, **self._to_user_model_attrs(data, provider))
        if ok:
          self.auth.set_session(self.auth.store.user_to_dict(user))

    # Redirect them to the next page.
    target = self.session.get('original_url')
    if target:
      del self.session['original_url']
      self.redirect(str(target))
    else:
      self.redirect('/profile')

  def logout(self):
    self.auth.unset_session()
    self.redirect('/')

  def _callback_uri_for(self, provider):
    return self.uri_for('auth_callback', provider=provider, _full=True)

  def _get_consumer_info_for(self, provider):
    """Returns a tuple (key, secret) for auth init requests."""
    return secrets.AUTH_CONFIG[provider]

  def _to_user_model_attrs(self, data, provider):
    attrs_map = self.USER_ATTRS[provider]
    user_attrs = {}
    for k, v in data.iteritems():
      if k in attrs_map:
        key = attrs_map[k]
        provider_key = '%s_%s' % (provider, key)
        if isinstance(key, str):
          user_attrs.setdefault(provider_key, v)
          user_attrs.setdefault(key, v)
        else:
          values = key(v)
          user_attrs.setdefault('%s_%s' % (provider, values[0]), values[1])
          user_attrs.setdefault(*values)

    return user_attrs
