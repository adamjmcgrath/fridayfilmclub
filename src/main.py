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

import admin
from api import contacts, leaderboard, question, users
import realtime
import settings
import suggest
import secrets
import tasks
import views


routes = [

    # Admin section.
    webapp_routes.PathPrefixRoute('/admin', [
        webapp2.Route('/addquestion', admin.AddEditQuestion, 'admin-add-question'),
        webapp2.Route(r'/editquestion/<key>', admin.AddEditQuestion,
            'admin-edit-question'),
        webapp2.Route('/questions', admin.Questions, 'admin-questions'),
        webapp2.Route('/posequestion', admin.PoseQuestion, 'admin-posequestion'),
        webapp2.Route('/posequestiontest/<key>', admin.PoseQuestionTest,
            'admin-posequestiontest'),
        webapp2.Route('/dryrun', admin.DryRun, 'admin-dryrun'),
        webapp2.Route('/deleteuserquestion', admin.DeleteUserQuestion,
            'admin-delete-user-question'),
    ]),
    webapp2.Route(r'/admin', admin.HomePage, 'admin-homepage'),

    # Tasks
    webapp2.Route(r'/tasks/cleanupanonymoususers', tasks.CleanUpAnonymousUsers,
        'tasks-cleananonusers'),
    webapp2.Route(r'/tasks/cleanupusertokens', tasks.CleanUpUserTokens,
        'tasks-cleanupusertokens'),
    webapp2.Route(r'/tasks/backup', tasks.ScheduledBackup, 'tasks-backup'),

    # Api.
    webapp2.Route(r'/api/question/<:.+>', question.Question, 'api-question'),
    webapp2.Route(r'/api/leaderboard/<:(week|all|league|\d+)>',
        leaderboard.LeaderBoard, 'api-leaderboard'),
    webapp2.Route(r'/api/contacts/<:.+>', contacts.Contacts, 'api-contacts'),
    webapp2.Route(r'/api/users/<:.+>', users.UserSearch, 'api-users'),
    webapp2.Route(r'/suggest/<:.+>', suggest.SuggestHandler, name='suggest'),

    # Authentication.
    webapp2.Route('/auth/<provider>',
        handler='auth.AuthHandler:_simple_auth', name='auth_login'),
    webapp2.Route('/auth/<provider>/callback',
        handler='auth.AuthHandler:_auth_callback', name='auth_callback'),
    webapp2.Route('/auth/<provider>/token',
        handler='auth.AuthHandler:_auth_token', name='auth_token'),
    webapp2.Route('/logout', handler='auth.AuthHandler:logout', name='logout'),

    # Main views (Authenticated).
    webapp2.Route(r'/question/<:.*>', views.Question, name='question'),
    webapp2.Route(r'/settings', views.Settings, name='settings'),
    webapp2.Route(r'/league/add', views.AddEditLeague, name='add-league'),
    webapp2.Route(r'/league/edit/<league_id:.*>', views.AddEditLeague,
        name='edit-league'),
    webapp2.Route(r'/league/<league_id:.*>', views.League, name='league'),

    # Realtime handlers.
    webapp2.Route(r'/_ah/channel/connected/', realtime.Connect),
    webapp2.Route(r'/_ah/channel/disconnected/', realtime.Disconnect),

    # Main views.
    webapp2.Route(r'/login', views.Login, name='login'),
    webapp2.Route(r'/register', views.Register, name='register'),
    webapp2.Route(r'/archive', views.Archive, name='archive'),
    webapp2.Route(r'/leaderboard', views.LeaderBoard, name='leader-board'),
    webapp2.Route(r'/leaderboard/<league:.*>', views.LeaderBoard,
        name='leader-board-league'),
    webapp2.Route(r'/highscores', views.HighScores, name='high-scores'),
    webapp2.Route(r'/highscores/<league:.*>', views.HighScores,
        name='high-scores-league'),
    webapp2.Route(r'/how', views.HowItWorks, name='how-it-works'),
    webapp2.Route(r'/u/<:[\w\d_]+>', views.Profile, name='profile'),
    webapp2.Route(r'/', views.HomePage, name='home'),
    webapp2.Route(r'/unsubscribe/<:\d+>', views.Unsubscribe, name='unsubscribe'),
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

app = webapp2.WSGIApplication(routes=routes,
                              debug=settings.DEBUG,
                              config=app_config)

def main():
  app.run()


if __name__ == '__main__':
  main()
