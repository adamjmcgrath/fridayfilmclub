#!/usr/bin/python

"""Indexing users."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging

from google.appengine.api import search


def tokenize(phrase):
  """ Create a list of partial tokens from s string. eg
  dog -> [d, do, dog]

  Args:
    phrase (str): The phrase to tokenize

  Return:
    list The list of tokens.
  """
  a = []
  for word in phrase.lower().split():
    j = 1
    while True:
      for i in range(len(word) - j + 1):
        a.append(word[i:i + j])
      if j == len(word):
        break
      j += 1
  return a


def index_users(users):
  """Creates or replaces a user document from a User model.

  Args:
    users (models.User[]): The User or list of users.
  """
  if type(users) is not list: users = [users]
  docs = []
  index = search.Index(name='users')

  for user in users:
    # Don't index admin users
    if user.is_admin:
      continue
    tokens = ','.join(tokenize('%s %s' % (user.name, user.username)))
    docs.append(search.Document(doc_id=str(user.key.id()),
                                language='en',
                                fields=[
                                    search.TextField(name='username',
                                                     value=user.username),
                                    search.TextField(name='name',
                                                     value=user.name),
                                    search.TextField(name='tokens',
                                                     value=tokens),
                                    search.TextField(name='pic',
                                                     value=user.pic_url())
                                ]))

  index.put(docs)

