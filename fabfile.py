#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Deploy the Friday Film Club application."""

from __future__ import with_statement

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging
import os
import re
import sys
from fabric.api import *

APPENGINE_PATH = os.environ['APPENGINE_SRC']
APPENGINE_DEV_APPSERVER =  os.path.join(APPENGINE_PATH, 'dev_appserver.py')
APPENGINE_APP_CFG =  os.path.join(APPENGINE_PATH, 'appcfg.py')

sys.path.append(APPENGINE_PATH)
import dev_appserver

dev_appserver.fix_sys_path()

env.gae_email = 'adamjmcgrath@gmail.com'
env.gae_src = './src'


def deploy(branch='dev', pull_request='false', tag=None):
  if pull_request != 'false':
    return
  version = re.sub(r'[\W_]', '-', branch)
  if tag:
    logging.info('Deploying TAG:%s to prod', tag)
    version = 'PROD'
  else:
    logging.info('Deploying VERSION:%s', version)

  local('python %s -V %s --oauth2 --oauth2_refresh_token=$OAUTH2_REFRESH_TOKEN update %s' %
        (APPENGINE_APP_CFG, version, env.gae_src))


def shell():
  with lcd(env.gae_src):
    local('python %s/remote_api_shell.py -s ffcapp.appspot.com' %
          APPENGINE_PATH)


def run_server(port='8080', clear_datastore=False, send_mail=True):
  command = '%s --port %s'

  if clear_datastore:
    command += ' --clear_datastore'
  if send_mail:
    command += ' --enable_sendmail=yes'

  command += ' %s'
  local(command % (APPENGINE_DEV_APPSERVER, port, env.gae_src))


def symlink_requirements():
  local('gaenv --lib src/pylib --no-import=true')


def compile_css():
  logging.info('Compiling CSS')
  local('mkdir -p src/static/css/')
  local('lessc --compress src/stylesheets/main.less > src/static/css/main.css')


def compile_js(part=None):
  parts = ['template', 'deps', 'quiz', 'leaderboard', 'settings', 'leagueform']
  local('mkdir -p src/static/js/')
  if part:
    parts = [part]
  for p in parts:
    local('scripts/compilejs.sh %s' % p)


def run_tests():
  local('nosetests --cover-html --nocapture --with-coverage --cover-inclusive '
        '--with-gae --gae-application=src/ --where=src/tests/ --gae-lib-root=%s'
        % APPENGINE_PATH)
