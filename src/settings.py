#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Main views of the Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import os
import re

import jinja2

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

is_dev = os.environ['SERVER_SOFTWARE'].startswith('Development')

_VALID_CALLBACK = re.compile('^\w+(\.\w+)*$')
