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
  a = set()
  for word in phrase.lower().split():
    j = 1
    while True:
      for i in range(len(word) - j + 1):
        a.add(word[i:i + j])
      if j == len(word):
        break
      j += 1
  return list(a)


def index_users(users):
  """Creates or replaces a user document from a User model.

  Args:
    users (models.User[]): The User or list of users.
  """
  if type(users) is not list: users = [users]
  docs = []
  index = search.Index(name='users')

  for user in users:
    # Don't index admin/anon users
    if user.is_admin or user.is_anonymous:
      continue
    tokens = ','.join(tokenize('%s %s' % (user.name, user.username)))
    docs.append(search.Document(doc_id=str(user.key.id()),
                                language='en',
                                fields=[
                                    search.TextField(
                                      name='username', value=user.username),
                                    search.TextField(
                                      name='name', value=user.name),
                                    search.TextField(
                                      name='tokens', value=tokens),
                                    search.TextField(
                                      name='pic', value=user.pic_url(size=20))
                                ]))

  index.put(docs)


def remove_users(user_keys):
  """Removes users from the user search index

  Args:
    user_keys (ndb.Key[]) Max 200 keys.
  """
  if type(user_keys) is not list: user_keys = [user_keys]
  index = search.Index(name='users')
  index.delete([str(key.id()) for key in user_keys])
