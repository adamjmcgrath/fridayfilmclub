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
import suggest
import views

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
    (r'/question/?(.+)?', views.Question),
    (r'/suggest/?(.+)?', suggest.SuggestHandler),

    (r'/api/question/?(.+)?', api.Question),

    (r'/', views.HomePage),
]

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'B1gtr0ubl31nl1ttl3ch1n4',
}

app = webapp2.WSGIApplication(routes=routes, debug=debug, config=config)

def main():
  app.run()


if __name__ == '__main__':
  main()
