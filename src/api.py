#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Question and Answer API - this contains the main quiz logic."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

from datetime import datetime
import logging

import auth
from datetime import datetime
from functools import partial
import json
import urllib

import baserequesthandler
import models
import realtime
import secrets
import twitter


from google.appengine.api import memcache, users, urlfetch
from google.appengine.ext import ndb

_MAX_CLUES = 4
_PASS = 'pass'
# Property map for normalising sorting across the different model.
_PROP_MAP = {
  'all': {
    'score': 'overall_score',
    'clues': 'overall_clues',
    'answered': 'questions_answered'
  },
  'week': {
    'score': 'score',
    'clues': 'clues_used'
  },
  'season': {
    'score': 'score',
    'clues': 'clues',
    'answered': 'questions_answered',
  }
}
_LB_CACHE = 'leaderboard_cache'


def set_leaderboard_cache(key, value, existing_cache=''):
  """Set the leaderboard cache."""
  if not existing_cache:
    existing_cache = memcache.get(_LB_CACHE) or ''
  cache_keys = existing_cache.split('|')
  cache_keys.append(key)
  memcache.set_multi({
    key: value,
    _LB_CACHE: '|'.join(cache_keys)
  })


def delete_leaderboard_cache():
  """Delete the leaderboard cache."""
  mc = memcache.Client()
  lb_cache = mc.get(_LB_CACHE)
  if lb_cache:
    mc.delete_multi_async(lb_cache.split('|') + [_LB_CACHE])


class Question(baserequesthandler.RequestHandler):
  """The main question/answer app logic - through a REST api."""

  @auth.login_required
  def get(self, question_id):
    self.get_or_post(question_id)

  @auth.login_required
  def post(self, question_id):
    # Get the users guess
    guess = self.request.get('guess')

    self.get_or_post(question_id, guess=guess)

  def get_or_post(self, question_id, guess=None):

    # Get the question and user.
    question = models.Question.get_by_id(int(question_id))
    user = self.current_user
    posed = question.posed

    # For debugging - create an arbitrary posed date for un-posed questions.
    if not posed and users.is_current_user_admin():
      posed = datetime.now()

    # Construct/get the user key.
    user_question_id = '%s-%s' % (question_id, user.key.id())
    user_question = models.UserQuestion.get_or_insert(user_question_id,
      question=question.key, user=user.key, user_is_admin=user.is_admin)

    to_put = []
    # Check if guess is correct, update UserQuestion.
    if guess and not user_question.complete:
      user_question.correct = (guess.strip() == str(question.answer_id))
      user_question.guesses.append(guess)
      num_guesses = len(user_question.guesses)

      if user_question.correct or num_guesses >= _MAX_CLUES:
        user_question.complete = True
        user_question.score = user_question.calculate_score(posed)
        user.overall_score += user_question.score
        user.overall_clues += num_guesses - 1
        user.questions_answered += 1
        question.answered += 1
        to_put.append(question)
        # Delete leaderboard memcache when a new score for the current
        # question comes in.
        if question.is_current:
          delete_leaderboard_cache()
          realtime.send_score_to_players(user, user_question.score)

        if question.season:
          user_season_id = '%s-%s' % (question.season.id(), user.key.id())
          user_season = models.UserSeason.get_or_insert(user_season_id,
            season=question.season, user=user.key, user_is_admin=user.is_admin)
          user_season.score += user_question.calculate_score(posed)
          user_season.clues += num_guesses - 1
          user_season.questions_answered += 1
          to_put.append(user_season)

      to_put.append(user_question)
      to_put.append(user)
      ndb.put_multi(to_put)

    # The number of the clues to show the user is one greater than the
    # number of guesses up to the maximum number of guesses.
    # If the user has had no guesses they get one clue.
    clue_increment = 0 if user_question.correct else 1
    clue_number = min((len(user_question.guesses) + clue_increment), _MAX_CLUES)

    guesses = []
    for g in user_question.guesses:
      if g == _PASS:
        # A blank guess is a "pass".
        guesses.append({})
      else:
        url = 'http://films-data.appspot.com/api?id=' + g
        film_dict = json.loads(urlfetch.fetch(url=url, follow_redirects=False).content)
        guesses.append({
          'title': film_dict['title'],
          'year': str(film_dict['year'])
        })

    response_obj = {
        'clues': [clue.get().to_json() for clue in question.clues[:clue_number]],
        'correct': user_question.correct,
        'guesses': guesses,
        'score': user_question.score or user_question.calculate_score(posed),
        'user': models.User.to_leaderboard_json(user)
    }

    # If the question is complete, reveal the correct answer to the user.
    if user_question.complete:
      response_obj['answer'] = {
        'key': question.answer_id,
        'title': question.answer_title,
        'year': question.answer_year,
      }
      response_obj['packshot'] = question.packshot_url(size=150)
      response_obj['imdb_url'] = question.imdb_url

    self.render_json(response_obj)


class LeaderBoard(baserequesthandler.RequestHandler):
  """Leader boards."""

  def get(self, duration):
    is_all = duration == 'all'
    is_week = duration == 'week'
    offset = self.request.get('offset') or 0
    limit = self.request.get('limit') or 20
    try:
      sort_props = _PROP_MAP[duration]
    except KeyError:
      sort_props = _PROP_MAP['season']
    sort = self.request.get('sort') or 'score'
    direction = self.request.get('dir') or 'asc'

    cache_key = '%s:%s:%s:%s:%s' % (str(duration), str(offset),
                                 str(limit), sort, direction)
    cached = memcache.get_multi([_LB_CACHE, cache_key])
    if cached.get(cache_key):
      self.render_json(cached.get(cache_key), is_string=True)
      return

    if sort:
      sort = ndb.GenericProperty(sort_props[sort])
      if not direction == 'asc':
        sort = -sort

    qo = ndb.QueryOptions(offset=int(offset), limit=int(limit))
    response_obj = {}

    if is_all:
      user_query = models.User.query(models.User.is_admin == False).order(sort)

      response_obj['count'] = user_query.count()
      response_obj['users'] = user_query.map(
                                  models.User.to_leaderboard_json, options=qo)

    elif is_week:
      question_query = models.Question.query(
          models.Question.is_current == True)

      question_key = question_query.get(keys_only=True)
      user_question_query = models.UserQuestion.query(
          models.UserQuestion.question == question_key,
          models.UserQuestion.complete == True,
          models.UserQuestion.user_is_admin == False).order(sort)
      response_obj['count'] = user_question_query.count()
      response_obj['users'] = user_question_query.map(
          models.UserQuestion.to_leaderboard_json, options=qo)

    else: # Should be the Season number.
      season = models.Season.get_by_id(duration)
      user_season_query = models.UserSeason.query(
          models.UserSeason.season == season.key,
          models.UserSeason.user_is_admin == False).order(sort)
      questions_in_season = models.Question.query(
          models.Question.season == season.key).count()
      response_obj['count'] = user_season_query.count()
      response_obj['users'] = user_season_query.map(
          partial(models.UserSeason.to_leaderboard_json, questions_in_season),
          options=qo)

    json_str = json.dumps(response_obj)
    set_leaderboard_cache(cache_key, json_str,
                          existing_cache=cached.get(_LB_CACHE, ''))
    self.render_json(json_str, is_string=True)


class Contacts(baserequesthandler.RequestHandler):

  def get(self, provider):

    cache_key = '%s:%s' % (
      self.current_user.to_dict().get(provider + '_token'), provider)
    cached = memcache.get(cache_key)

    if cached:
      self.render_json(json.loads(cached))
      return
    else:
      json_list = []

    if provider == 'google':
      json_list = self.get_google_contacts()

    if provider == 'facebook':
      json_list = self.get_facebook_friends()

    if provider == 'twitter':
      json_list = self.get_twitter_followers()

    memcache.add(cache_key, json.dumps(json_list), time=3600)
    self.render_json(json_list)

  def get_google_contacts(self):
    refresh_token = self.current_user.google_refresh_token
    json_list = []
    if refresh_token:

      #  Convert the access token to refresh_token
      app_id, app_secret, app_scope = secrets.AUTH_CONFIG['google']
      data = urllib.urlencode({
            'client_id': app_id,
            'client_secret': app_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
      })
      token_response = urlfetch.fetch(method='POST',
          url='https://accounts.google.com/o/oauth2/token', payload=data)
      logging.info(token_response.content)
      tokens = json.loads(token_response.content)
      google_token = tokens['access_token']

      # Request the contacts
      response = urlfetch.fetch(
        'https://www.google.com/m8/feeds/contacts/default/full/?alt=json&max-results=9999',
        headers={'Authorization': 'Bearer %s' % google_token})


      for entry in json.loads(response.content)['feed']['entry']:
        email = None
        try:
          email = (x['address'] for x in entry['gd$email'] if x['primary'] == 'true').next()
        except KeyError:
          pass

        name = entry['title']['$t']

        try:
          pic_type = 'http://schemas.google.com/contacts/2008/rel#photo'
          pic = (x['href'] for x in entry['link'] if x['rel'] == pic_type).next()
          pic += '?access_token=' + google_token
        except:
          pic = '/static/img/anon.gif'

        if name and email:
          json_list.append({
            'name': entry['title']['$t'],
            'email': email,
            'pic': pic
          })

    return json_list

  def get_facebook_friends(self):
    u = self.current_user
    app_id, app_secret, app_scope = secrets.AUTH_CONFIG['facebook']
    # facebook_token = u.facebook_token
    facebook_token = app_id + '|' + app_secret
    facebook_uid = u.facebook_uid
    json_list = []
    if facebook_token:
      url = ('https://graph.facebook.com/%s/friends?access_token=%s&limit=500&fields=username,name'
             % (facebook_uid, facebook_token.strip()))
      while url:
        logging.info('Getting facebook url: %s', url)
        json_obj = json.loads(urlfetch.fetch(url).content)
        json_list = json_list + json_obj['data']
        url = json_obj['paging'].get('next')
      self.set_json_content_type()

    return json_list

  def get_twitter_followers(self):
    u = self.current_user
    twitter_token = self.current_user.twitter_token
    twitter_token_secret = self.current_user.twitter_token_secret
    json_list = []
    if twitter_token and twitter_token_secret:
      cursor = -1

      while cursor:
        url = 'https://api.twitter.com/1.1/followers/list.json'
        params = {
          'screen_name': u.twitter_name,
          'skip_status': 'true',
          'include_user_entities': 'false',
          'cursor': str(cursor)
        }

        auth_header = twitter.header_string_for_request(url, params, 'GET',
                                                        twitter_token,
                                                        twitter_token_secret)

        url += '?' + urllib.urlencode(params)
        response = urlfetch.fetch(url, headers={'Authorization': auth_header})

        json_obj = json.loads(response.content)
        cursor = json_obj.get('next_cursor')
        json_list += json_obj['users']

    return [{
      'pic': u['profile_image_url'],
      'id': u['screen_name'],
      'name': u['name']
    } for u in json_list]

