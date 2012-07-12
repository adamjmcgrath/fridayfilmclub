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


def get_films_from_slug(slug):
  """docstring for get_films_from_slug"""
  films = models.Film.all().filter('title_slug = ', slug).fetch(10) or []
  film_keys = [f.key() for f in films]

  film_index = models.FilmIndex.get_by_key_name(slug)
  
  if not film_index:
    return films

  films_from_index = models.Film.get(film_index.films)  
  films_from_index_sorted = sorted(films_from_index, key=lambda m: m.year, reverse=True)

  for film in films_from_index_sorted:
    if film.key() not in film_keys:
      films.append(film)

  return films


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

    get_films_from_slug(prefix)

    self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    if memcached and not debug:
      if add_callback:
        memcached = '%s(%s)' % (callback, memcached)
      return webapp2.Response(memcached)

    films = get_films_from_slug(prefix)
    if films:
      films_response = [f.to_dict() for f in films]
      indent = 2 if debug else None
      films_json = json.dumps(films_response, indent=indent)
      if not debug:
        memcache.set(prefix, films_json)
      if add_callback:
        films_json = '%s(%s)' % (callback, films_json)
      return webapp2.Response(films_json)
    else:
      return webapp2.Response('')
