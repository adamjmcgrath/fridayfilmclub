#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""The MapReduce functions for Friday Film Club."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import csv
import cStringIO as StringIO
import logging

from google.appengine.ext import db

from mapreduce import base_handler, mapreduce_pipeline
from mapreduce import operation as op

import models

FILMS_PER_INDEX = 10



def add_film_map(input_tuple):
  """Add films to the data store."""
  io = StringIO.StringIO(input_tuple[1])
  row = csv.reader(io).next()
  year = row[0]
  title = row[1]
  title_slug = models.slugify_splaceless(title)
  film_entity = models.Film(
      key_name='%s-%s' % (year, title_slug),
      title=unicode(title, 'utf-8'),
      title_slug=title_slug,
      year=int(year),)
  
  try:
    film_entity.grossing = int(row[2])
  except IndexError:
    pass

  yield op.db.Put(film_entity)


def film_index_map(entity):
  """Index each film title."""
  key = entity.key()
  key_name = key.name()
  logging.info('Mapping: %s' % key_name)
  words = key_name.split('-')[1:]
  starts = []
  for i in range(0, len(words)):
    start = ''.join(words[i:])
    for j in range(1, len(start) + 1):
      pfx = start[:j]
      if pfx not in starts:
        starts.append(pfx)
        yield (pfx, '%d/%d/%s/%s' % (entity.year, entity.grossing or 0, entity.title_slug, key))


def film_index_reduce(word, films):
  """Reduce the indexed film titles and add the indexes to the datastore."""
  logging.info('Reducing: %s' % word)

  # Sort by year.
  films_sorted_year = sorted(
      films, key=lambda m: m.split('/')[0], reverse=True)
  # Then sort by grossing.
  films_sorted_grossing = sorted(films_sorted_year,
      key=lambda m: int(m.split('/')[1]), reverse=True)
  # Then put exact matches at the top.
  films_sorted_match = sorted(films_sorted_grossing,
      key=lambda m: m.split('/')[2] == word, reverse=True)

  index_entity = models.FilmIndex(
      key_name=word,
      films=[db.Key(m.split('/')[3]) for m in films_sorted_match][:FILMS_PER_INDEX],)

  yield op.db.Put(index_entity)


class IndexerPipeline(base_handler.PipelineBase):
  """A map reduce pipeline for indexing film titles."""

  def run(self):
    yield mapreduce_pipeline.MapreducePipeline(
        'index_films',
        'map_reduce.film_index_map',
        'map_reduce.film_index_reduce',
        'mapreduce.input_readers.DatastoreInputReader',
        mapper_params={
            'entity_kind': 'models.Film',
        })
