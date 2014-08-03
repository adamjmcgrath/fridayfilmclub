#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Main views of the Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import os

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
FMJ_EMAIL_SHORT = 'fmj@fridayfilmclub.com'
FMJ_EMAIL = 'Film Master Jack <%s>' % FMJ_EMAIL_SHORT
ENVIRONMENT = ({
  'www.fridayfilmclub.com': 'prod',
  'dev.ffcapp.appspot.com': 'staging',
}).get(os.environ.get('HTTP_HOST'), 'local')
