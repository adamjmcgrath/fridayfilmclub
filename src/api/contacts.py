#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Contacts API"""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import logging

import json
import urllib

import baserequesthandler
import secrets
import twitter

from google.appengine.api import memcache, urlfetch

_MAX_CLUES = 4
_PASS = 'pass'


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
      app_id, app_secret, app_scope = secrets.get_auth_config('google', 'prod')
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
    app_id, app_secret, app_scope = secrets.get_auth_config('facebook', 'prod')
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

