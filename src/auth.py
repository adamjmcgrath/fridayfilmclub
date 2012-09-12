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



class AuthHandler(baserequesthandler.RequestHandler, SimpleAuthHandler):
  """Authentication handler for all kinds of auth."""

  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)
    
    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session(self):
    """Returns a session using the default cookie key"""
    return self.session_store.get_session()

  def _on_signin(self, data, auth_info, provider):
    """Callback whenever a new or existing user is logging in.
    data is a user info dictionary.
    auth_info contains access token or oauth token and secret.
    
    See what's in it with logging.info(data, auth_info)
    """

    auth_id = '%s:%s' % (provider, data['id'])

    logging.info(auth_id)

    # 1. check whether user exist, e.g.
    #    User.get_by_auth_id(auth_id)
    #
    # 2. create a new user if it doesn't
    #    User(**data).put()
    #
    # 3. sign in the user
    #    self.session['_user_id'] = auth_id
    #
    # 4. redirect somewhere, e.g. self.redirect('/profile')
    #
    # See more on how to work the above steps here:
    # http://webapp-improved.appspot.com/api/webapp2_extras/auth.html
    # http://code.google.com/p/webapp-improved/issues/detail?id=20
    

  def logout(self):
    self.auth.unset_session()
    self.redirect('/')

  def _callback_uri_for(self, provider):
    return self.uri_for('auth_callback', provider=provider, _full=True)

  def _get_consumer_info_for(self, provider):
    """Get he apps OAuth credentials.

    Args:
      provider: The OAuth provider identifier (twitter, facebook or google)
    
    Returns:
      a tuple (key, secret) for auth init requests.
      For OAuth 2.0 it also returns a scope, e.g.
      ('my app id', 'my app secret', 'email,user_about_me')
    """
    return secrets.AUTH_CONFIG[provider]
