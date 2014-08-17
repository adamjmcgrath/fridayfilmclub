#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""App Engine config."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'gaenv_lib'))

# Enabled copying data from the movieautocomplete app.
remoteapi_CUSTOM_ENVIRONMENT_AUTHENTICATION = (
    'HTTP_X_APPENGINE_INBOUND_APPID', ['movieautocomplete'])