#!/usr/bin/python
#
# Copyright 2012 Friday Film Club. All Rights Reserved.

"""Secret keys."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import settings


# webapp2 session secret key
SESSION_KEY = '[YOUR-KEY]'

# Google OAuth 2
GOOGLE_APP_ID = '[YOUR-KEY]'
GOOGLE_APP_SECRET = '[YOUR-KEY]'
GOOGLE_SCOPE = ('https://www.google.com/m8/feeds '
                'https://www.googleapis.com/auth/userinfo.profile '
                'https://www.googleapis.com/auth/userinfo.email')
GOOGLE_APP_ID_DEV = '[YOUR-KEY]'
GOOGLE_APP_SECRET_DEV = '[YOUR-KEY]'
GOOGLE_APP_ID_STAGING = '[YOUR-KEY]'
GOOGLE_APP_SECRET_STAGING = '[YOUR-KEY]'

# Facebook OAuth 2
FACEBOOK_APP_ID = '[YOUR-KEY]'
FACEBOOK_APP_SECRET = '[YOUR-KEY]'
FACEBOOK_SCOPE = 'user_about_me,email'
FACEBOOK_APP_ID_DEV = '[YOUR-KEY]'
FACEBOOK_APP_SECRET_DEV = '[YOUR-KEY]'
FACEBOOK_APP_ID_STAGING = '[YOUR-KEY]'
FACEBOOK_APP_SECRET_STAGING = '[YOUR-KEY]'

# Twitter OAuth 1.0a
TWITTER_CONSUMER_KEY = '[YOUR-KEY]'
TWITTER_CONSUMER_SECRET = '[YOUR-KEY]'
TWITTER_CONSUMER_KEY_DEV = '[YOUR-KEY]'
TWITTER_CONSUMER_SECRET_DEV = '[YOUR-KEY]'
TWITTER_CONSUMER_KEY_STAGING = '[YOUR-KEY]'
TWITTER_CONSUMER_SECRET_STAGING = '[YOUR-KEY]'

# Auth config
_CONFIG = {
  'google': (GOOGLE_APP_ID, GOOGLE_APP_SECRET, GOOGLE_SCOPE),
  'facebook': (FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_SCOPE),
  'twitter': (TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET),
}

_CONFIG_DEV = {
  'google': (GOOGLE_APP_ID_DEV, GOOGLE_APP_SECRET_DEV, GOOGLE_SCOPE),
  'facebook': (FACEBOOK_APP_ID_DEV, FACEBOOK_APP_SECRET_DEV, FACEBOOK_SCOPE),
  'twitter': (TWITTER_CONSUMER_KEY_DEV, TWITTER_CONSUMER_SECRET_DEV),
}

_CONFIG_STAGING = {
  'google': (GOOGLE_APP_ID_STAGING, GOOGLE_APP_SECRET_STAGING, GOOGLE_SCOPE),
  'facebook': (FACEBOOK_APP_ID_STAGING,
               FACEBOOK_APP_SECRET_STAGING,
               FACEBOOK_SCOPE),
  'twitter': (TWITTER_CONSUMER_KEY_STAGING, TWITTER_CONSUMER_SECRET_STAGING),
}

def get_auth_config(provider, environment):
  return ({
    'local': _CONFIG_DEV,
    'staging': _CONFIG_STAGING,
  }).get(environment, _CONFIG)[provider]