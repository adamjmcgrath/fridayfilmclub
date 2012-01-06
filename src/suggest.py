#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Main views of the Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import json
import logging
import os
import re

import webapp2
from google.appengine.api import memcache

import models

VALID_CALLBACK = re.compile('^\w+(\.\w+)*$')



class SuggestHandler(webapp2.RequestHandler):
  """Returns JSON sugesting film titles given a starting string."""

  def get(self, prefix):
    debug = self.request.get('debug')
    callback = self.request.get('callback')
    add_callback = callback and VALID_CALLBACK.match(callback)
    if not prefix:
      return webapp2.Response('')

    prefix = prefix.strip()    
    memcached = memcache.get(prefix)
    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    if memcached and not debug:
      if add_callback:
        memcached = '%s(%s)' % (callback, memcached)
      return webapp2.Response(memcached)

    film_index = models.FilmIndex.get_by_key_name(prefix)
    if film_index:
      films = models.Film.get(film_index.films)
      films_sorted = sorted(films, key=lambda m: m.year, reverse=True)
      films_response = [f.to_dict() for f in films_sorted]
      indent = 2 if debug else None
      films_json = json.dumps(films_response, indent=indent)
      if not debug:
        memcache.set(prefix, films_json)
      if add_callback:
        films_json = '%s(%s)' % (callback, films_json)
      return webapp2.Response(films_json)
    else:
      return webapp2.Response('')
