#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Deploy the Friday Film Club application."""

from __future__ import with_statement

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import functools
import os
import sys
from fabric.api import *
from fabric.colors import green, red, yellow
import datetime
import re
import yaml

APPENGINE_PATH = os.environ['APPENGINE_SRC']
APPENGINE_DEV_APPSERVER =  os.path.join(APPENGINE_PATH, 'dev_appserver.py')
APPENGINE_APP_CFG =  os.path.join(APPENGINE_PATH, 'appcfg.py')
VERSIONS = {
  'devel': 'dev',
  'master': 'prod',
}

env.gae_email = 'adamjmcgrath@gmail.com'
env.gae_src = './src'

def fix_appengine_path():
  EXTRA_PATHS = [
    APPENGINE_PATH,
    os.path.join(APPENGINE_PATH, 'lib', 'antlr3'),
    os.path.join(APPENGINE_PATH, 'lib', 'django'),
    os.path.join(APPENGINE_PATH, 'lib', 'fancy_urllib'),
    os.path.join(APPENGINE_PATH, 'lib', 'ipaddr'),
    os.path.join(APPENGINE_PATH, 'lib', 'webob'),
    os.path.join(APPENGINE_PATH, 'lib', 'yaml', 'lib'),
  ]
  
  sys.path = EXTRA_PATHS + sys.path

fix_appengine_path()


def deploy(branch='devel', token='', pull_request='false'):
  if pull_request != 'false':
    return
  version = VERSIONS.get(branch)

  if version:
    local('python %s -V %s --oauth2 --oauth2_refresh_token=%s update %s' %
          (APPENGINE_APP_CFG, version, token, env.gae_src))


def set_app_version(branch):
  version = VERSIONS.get(branch)
  if version:
    yaml_path = 'src/app.yaml'
    app_yaml = yaml.load(open(yaml_path))
    app_yaml['version'] = version
    with open(yaml_path, 'w') as app_yaml_file:
      app_yaml_file.write(yaml.dump(app_yaml, default_flow_style=False))


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


# Compile CSS/JS

def compile_css():
  print 'Compiling CSS'
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
