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
    """foo"""
    prefix = prefix and prefix.strip()

    if not prefix:
      return webapp2.Response('')

    self.set_json_content_type()

    url = 'http://films-data.appspot.com/api?q=' + prefix
    content = urlfetch.fetch(url=url, follow_redirects=False).content
    return self.response.out.write(content)

    # memcached = memcache.get(prefix + callback)
    # if memcached and self.is_debug_mode():
    #   return webapp2.Response(memcached)
    #
    # film_index = models.FilmIndex.get_by_id(prefix)
    #
    # if film_index:
    #   films = ndb.get_multi(film_index.films)
    #   return self.render_json([f.to_dict() for f in films])
    # else:
    #   return self.render_empty()
