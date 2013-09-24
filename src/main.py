#!/usr/bin/python2.7
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging
import os
import sys

import webapp2
from webapp2_extras import routes as webapp_routes

if 'third_party' not in sys.path:
  sys.path[0:0] = ['third_party']

import admin
import api
import settings
import suggest
import secrets
import views


routes = [

    # Admin section.
    webapp_routes.PathPrefixRoute('/admin', [
        webapp2.Route('/addfilms', admin.AddFilms, 'admin-add-films'),
        webapp2.Route('/addfilmshandler', admin.AddFilmsHandler,
            'admin-add-films-handler'),
        webapp2.Route('/addfilmsdone', admin.AddFilmsDone,
            'admin-add-films-done'),
        webapp2.Route('/addquestion', admin.AddEditQuestion, 'admin-add-question'),
        webapp2.Route(r'/editquestion/<key>', admin.AddEditQuestion,
            'admin-edit-question'),
        webapp2.Route('/indexfilms', admin.IndexFilms, 'admin-index-films'),
        webapp2.Route('/questions', admin.Questions, 'admin-questions'),
        webapp2.Route('/posequestion/<key>', admin.PoseQuestion, 'admin-posequestion'),
    ]),
    webapp2.Route(r'/admin', admin.HomePage, 'admin-homepage'),

    # Api.
    webapp2.Route(r'/api/question/<:.+>', api.Question, 'api-question'),
    webapp2.Route(r'/suggest/<:.+>', suggest.SuggestHandler, name='suggest'),

    # Authentication.
    webapp2.Route('/auth/<provider>',
        handler='auth.AuthHandler:_simple_auth', name='auth_login'),
    webapp2.Route('/auth/<provider>/callback',
        handler='auth.AuthHandler:_auth_callback', name='auth_callback'),
    webapp2.Route('/logout', handler='auth.AuthHandler:logout', name='logout'),

    # Main views (Authenticated).
    webapp2.Route(r'/question/<:.+>', views.Question, name='question'),
    webapp2.Route(r'/profile', views.Profile, name='profile'),
    webapp2.Route(r'/login', views.Login, name='login'),

    # Main views.
    webapp2.Route(r'/archive', views.Archive, name='archive'),
    webapp2.Route(r'/leaderboard', views.LeaderBoard, name='leader-board'),
    webapp2.Route(r'/how', views.HowItWorks, name='how-it-works'),
    webapp2.Route(r'/', views.HomePage, name='home'),
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

app = webapp2.WSGIApplication(routes=routes, debug=settings.debug, config=app_config)

def main():
  app.run()


if __name__ == '__main__':
  main()
