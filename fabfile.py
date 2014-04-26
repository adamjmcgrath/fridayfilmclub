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

APPENGINE_PATH = os.environ['APPENGINE_SRC']
APPENGINE_DEV_APPSERVER =  os.path.join(APPENGINE_PATH, 'dev_appserver.py')
APPENGINE_APP_CFG =  os.path.join(APPENGINE_PATH, 'appcfg.py')

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
from google.appengine.api import appinfo



def include_appcfg(func):
  """Decorator that ensures the current Fabric env has a GAE app.yaml config
  attached to it."""
  @functools.wraps(func)
  def decorated_func(*args, **kwargs):
    if not hasattr(env, 'app'):
      try:
        appcfg = appinfo.LoadSingleAppInfo(open('%s/app.yaml' % env.gae_src))
      except IOError:
        abort('You must be in the App Engine application root.')
      env.app = appcfg
    return func(*args, **kwargs)
  return decorated_func


def last_tag():
  print yellow('Last tag: %s' % get_last_tag_match())


def tgz():
  tag = get_last_tag_match()
  local('git archive --format=tar %s | gzip > tag_%s.tar.gz' % (tag, tag))


@include_appcfg
def deploy(tag=None):
  if not is_working_directory_clean():
    abort('Working directory should be clean before deploying.')

  compile_css()
  compile_js()

  prepare_deploy(tag)
  local('python %s -A %s -V %s --email=%s update %s' % (APPENGINE_APP_CFG,
      env.app.application, env.app.version, env.gae_email, env.gae_src))
  end_deploy()
  commit()


@include_appcfg
def shell():
  with lcd(env.gae_src):
    local('python %s/remote_api_shell.py -s ffcapp.appspot.com' %
          APPENGINE_PATH)


def run(port='8080', clear_datastore=False, send_mail=True):
  command = '%s --port %s'

  if clear_datastore:
    command += ' --clear_datastore'
  if send_mail:
    command += ' --enable_sendmail=yes'

  command += ' %s'
  local(command % (APPENGINE_DEV_APPSERVER, port, env.gae_src))


def commit(branch='master'):
  if not is_working_directory_clean():
    abort('Working directory should be clean before pushing.')
  print yellow('Updating remote repository.')
  local('git push --tags origin %s' % branch)


def prepare_deploy(tag=None):
  print yellow('Preparing the deployement.')

  if tag != None:
    env.deployement_tag = tag
  else:
    do_tag()

  # Set the app version to the git tag.
  print 'env.deployement_tag:'
  print env.deployement_tag
  env.app.version = env.deployement_tag
  
  # Check out a clean copy.
  deploy_path = local('mktemp -d -t %s' % env.app.application, capture=True)
  local('git clone . %s' % deploy_path)

  with lcd(deploy_path):
    local('git checkout %s' % env.deployement_tag)
    local('find . -name ".git*" | xargs rm -rf')
    print yellow('App: %s' % env.app.application)
    print yellow('Ver: %s' % env.app.version)
  
  env.deploy_path = deploy_path


def end_deploy():
  print yellow('Cleaning up after the deploy.')
  local('rm -rf %s' % env.deploy_path)


def check_if_last_version():
  branch = local('git branch --no-color 2> /dev/null | '
    'sed -e "/^[^*]/d"', capture=True).replace('* ', '').strip()
  local_sha = local('git log --pretty=format:%H HEAD -1', capture=True).strip()
  origin_sha = local(
      'git log --pretty=format:%%H %s -1' % branch, capture=True).strip()
  if local_sha != origin_sha:
    abort("""
    Your %s branch is not up to date with origin/%s.
    Please make sure you have pulled and pushed all code before deploying:

    git pull origin %s
    #run tests, etc
    git push origin %s

    """ % (branch, branch, branch, branch))


def get_last_tag_match():
  tags = local('git tag -l', capture=True)
  if len(tags) == 0:
    return None
  tags = tags.split()
  tags.sort()
  return tags[-1]


def do_tag():
  (last_tag_name, next_tag_name) = get_tags_name()

  if need_to_tag('HEAD', last_tag_name):
    local('git tag -a -m "tagging code for deployment" %s' % next_tag_name)
    env.deployement_tag = next_tag_name
  else:
    env.deployement_tag = last_tag_name


def update_tag(tag_name, from_tag):
  if get_last_tag_match() != None:
    local('git tag -d %s' % tag_name)
  local('git tag -a -m "updating %s to %s" %s %s' % (tag_name, from_tag, tag_name, from_tag))


def need_to_tag(version1, version2):
  sha_version1 = local(
      'git log --pretty=format:%%H %s -1' % version1, capture=True)
  if version2:
    sha_version2 = local(
        'git log --pretty=format:%%H %s -1' % version2, capture=True)
    if sha_version1 == sha_version2:
      print yellow('No need to tag, the last %s tag is the same as the current')
      return False
  return True


def is_working_directory_clean():
  status = local('git status --short',
      capture=True)
  if status: # There are pending files.
    print red('Working directory not clean.')
    return False
  print yellow('Working directory clean.')
  return True


def get_tags_name():
  today = datetime.date.today()
  next_tag_name = ('%i-%.2i-%.2i' %
      (today.year, today.month, today.day))

  last_tag_name = get_last_tag_match()
  if last_tag_name == None:
    num = 1
  else:
    match = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}-([0-9]*)',
        last_tag_name)
    num = int(match.group(1)) + 1

  next_tag_name = '%s-%.3i' % (next_tag_name, num)
  print yellow('Last tag name: %s' % last_tag_name)
  print yellow('Next tag name: %s' % next_tag_name)
  return (last_tag_name, next_tag_name)


# Compile CSS/JS

def compile_css():
  print 'Compiling CSS'
  local('mkdir -p src/static/css/')
  local('lessc --compress src/stylesheets/main.less > src/static/css/main.css')


def compile_js(part=None):
  parts = ['deps', 'template', 'quiz', 'leaderboard', 'settings',
           'requestinvite']
  local('mkdir -p src/static/js/')
  if part:
    parts = [part]
  for p in parts:
    local('scripts/compilejs.sh %s' % p)


def run_tests():
  local('nosetests --with-gae --gae-application=src/ --where=src/tests/')
