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

import baserequesthandler
import models


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

    films = get_films_from_slug(prefix)
    if films:
      return self.render_json([f.to_dict() for f in films])
    else:
      return self.render_empty()
