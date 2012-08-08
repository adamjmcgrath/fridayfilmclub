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

import settings

_JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
_TEMPLATE_PATH = '/templates/jinja/'
_VALID_CALLBACK = re.compile('^\w+(\.\w+)*$')

class RequestHandler(webapp2.RequestHandler):
  """docstring for Base"""

  def is_debug_mode(self):
    """docstring for is_debug_mode"""
    return (os.environ['SERVER_SOFTWARE'].startswith('Development') and
        self.request.get('debug') != 'false')

  def render_template(self, template_path, template_obj):
    """docstring for render_to_template"""
    template = _JINJA_ENV.get_template(
        posixpath.join(_TEMPLATE_PATH, template_path))

    template_obj['debug'] = self.is_debug_mode();

    return webapp2.Response(template.render(template_obj))

  def get_json_callback(self):
    """Get json callback"""
    callback = self.request.get('callback')
    if callback and _VALID_CALLBACK.match(callback):
      return callback
    else:
      return ''

  def set_json_content_type(self):
    """foo"""
    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

  def render_json(self, json_obj):
    
    
    logging.info(json_obj)
    
    """docstring for render_json"""
    indent = 2 if self.is_debug_mode() else None
    callback = self.get_json_callback()

    json_response = json.dumps(json_obj, indent=indent)

    if callback:
      json_response = '%s(%s)' % (callback, json_response)

    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

    return webapp2.Response(json_response)

  def render_empty(self):
    """foo"""
    return webapp2.Response('')

