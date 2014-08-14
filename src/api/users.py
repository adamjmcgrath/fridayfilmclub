#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

"""Users API."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging

import baserequesthandler


from google.appengine.api import search

_SEARCH_LIMIT = 10


def get_users_from_query(q):
  """Create a search query for users from a query string.

  Args:
    q (str): The query string.

  Return:
    SearchResults
  """

  query = search.Query(query_string=q)
  index = search.Index(name='users')

  return index.search(query)


def doc_to_dict(doc):
  """Create a dictionary for json conversion from a search document.

  Args:
    SearchDocument

  Return:
    dict
  """
  fields = {}
  for f in doc.fields:
    fields[f.name] = f.value
  return {
    'key': doc.doc_id,
    'name': fields['name'],
    'username': fields['username'],
    'pic': fields['pic']
  }


class UserSearch(baserequesthandler.RequestHandler):
  """Search for users."""

  def get(self, query):

    results = get_users_from_query(query).results

    self.render_json([doc_to_dict(result) for result in results])
