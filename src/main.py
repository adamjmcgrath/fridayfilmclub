#!/usr/bin/python2.7
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging
import os

import webapp2

import admin
import api
import auth
import suggest
import secrets
import views

if 'third_party' not in sys.path:
    sys.path[0:0] = ['third_party']

debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

routes = [
    (r'/admin/addfilms/?', admin.AddFilms),
    (r'/admin/addfilmshandler/?', admin.AddFilmsHandler),
    (r'/admin/addfilmsdone/?', admin.AddFilmsDone),
    webapp2.Route(r'/admin/editquestion/<key>', admin.AddEditQuestion),
    (r'/admin/addquestion/?', admin.AddEditQuestion),
    (r'/admin/indexfilms/?', admin.IndexFilms),
    (r'/admin/questions/?', admin.Questions),
    (r'/admin/?', admin.HomePage),

    (r'/api/question/?(.+)?', api.Question),

    Route('/auth/<provider>', handler='handlers.AuthHandler:_simple_auth', name='auth_login'),
    Route('/auth/<provider>/callback', handler='handlers.AuthHandler:_auth_callback', name='auth_callback'),
    Route('/logout', handler='handlers.AuthHandler:logout', name='logout')

    (r'/question/?(.+)?', views.Question),

    (r'/suggest/?(.+)?', suggest.SuggestHandler),



    (r'/', views.HomePage),
]

app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': secrets.SESSION_KEY
  },
  'webapp2_extras.auth': {
    'user_attributes': []
  }
}

app = webapp2.WSGIApplication(routes=routes, debug=debug, config=app_config)

def main():
  app.run()


if __name__ == '__main__':
  main()
