#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Base request handler class."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'


import json
import logging
import os
import posixpath
import re

import jinja2
import webapp2
from webapp2_extras import auth, sessions

import settings

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
JINJA_ENV.globals.update({'uri_for': webapp2.uri_for})
TEMPLATE_PATH = '/templates/jinja/'
VALID_CALLBACK = re.compile('^\w+(\.\w+)*$')



class RequestHandler(webapp2.RequestHandler):
  """docstring for Base"""

  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)
    try:
      # Dispatch the request.
      return webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session(self):
    """Returns a session using the default cookie key"""
    return self.session_store.get_session()

  @webapp2.cached_property
  def auth(self):
      return auth.get_auth()

  @webapp2.cached_property
  def current_user(self):
    """Returns currently logged in user"""
    user_dict = self.auth.get_user_by_session()
    return self.auth.store.user_model.get_by_id(user_dict['user_id'])

  @webapp2.cached_property
  def logged_in(self):
    """Returns true if a user is currently logged in, false otherwise."""
    return self.auth.get_user_by_session() is not None

  def is_debug_mode(self):
    """docstring for is_debug_mode"""
    debug_param = self.request.get('debug')
    debug_env = os.environ['SERVER_SOFTWARE'].startswith('Development')
    return debug_param == 'true' or (debug_env and debug_param != 'false')

  def generate_template(self, template_path, template_obj):
    """Create the template output."""
    template = JINJA_ENV.get_template(
        posixpath.join(TEMPLATE_PATH, template_path))
    values = {
      'url_for': self.uri_for,
      'logged_in': self.logged_in,
      'debug': self.is_debug_mode(),
    }
    if self.logged_in:
      values['user'] = self.current_user
    # Add manually supplied template values
    values.update(template_obj)
    return template.render(values)

  def render_template(self, template_path, template_obj):
    """docstring for render_template"""
    return webapp2.Response(self.generate_template(template_path, template_obj))

  def get_json_callback(self):
    """Get json callback"""
    callback = self.request.get('callback')
    if callback and VALID_CALLBACK.match(callback):
      return callback
    else:
      return ''

  def set_json_content_type(self):
    """Set the content type to application/json."""
    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

  def render_json(self, json_obj, is_string=False):
    """docstring for render_json"""
    indent = 2 if self.is_debug_mode() else None
    callback = self.get_json_callback()
    if is_string:
      json_response = json_obj
    else:
      json_response = json.dumps(json_obj, indent=indent)
    if callback:
      json_response = '%s(%s)' % (callback, json_response)
    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return webapp2.Response(json_response)

  def render_empty(self):
    """Render an empty response."""
    return webapp2.Response('')

