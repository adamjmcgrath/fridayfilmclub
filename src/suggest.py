#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Main views of the Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging
import os
import re

import webapp2
from google.appengine.api import memcache, urlfetch
from google.appengine.ext import ndb

import baserequesthandler
import models



class SuggestHandler(baserequesthandler.RequestHandler):
  """Returns JSON suggesting film titles given a starting string."""

  def get(self, prefix):
    """Use the films data api to get film suggestions."""
    prefix = prefix and prefix.strip()

    if not prefix:
      return webapp2.Response('')

    self.set_json_content_type()

    memcached = memcache.get(prefix)
    if memcached and not self.is_debug_mode():
      return webapp2.Response(memcached)

    url = 'http://films-data.appspot.com/api?q=' + prefix
    content = urlfetch.fetch(url=url, follow_redirects=False).content
    return self.response.out.write(content)
