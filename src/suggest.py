#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Main views of the Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging
import os
import re

import webapp2
from google.appengine.api import memcache
from google.appengine.ext import ndb

import baserequesthandler
import models



class SuggestHandler(baserequesthandler.RequestHandler):
  """Returns JSON sugesting film titles given a starting string."""

  def get(self, prefix):
    """foo"""
    callback = self.get_json_callback()
    prefix = prefix and prefix.strip()

    if not prefix:
      return webapp2.Response('')

    memcached = memcache.get(prefix + callback)
    if memcached and self.is_debug_mode():
      self.set_json_content_type()
      return webapp2.Response(memcached)

    film_index = models.FilmIndex.get_by_id(prefix)

    if film_index:
      films = ndb.get_multi(film_index.films)
      return self.render_json([f.to_dict() for f in films])
    else:
      return self.render_empty()
