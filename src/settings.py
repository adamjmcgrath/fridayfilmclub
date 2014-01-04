#!/usr/bin/python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Main views of the Friday Film Club app."""

__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import os
import datetime
from dateutil import relativedelta
import math

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
START_DATE = datetime.datetime(2013, 12, 20, 3)
WEEKS_PER_SEASON = 12
DAYS_PER_WEEK = 7


def get_week_season_from_date(date):
  days = relativedelta.relativedelta(date, START_DATE).days
  weeks = math.ceil(days / float(DAYS_PER_WEEK))
  season = math.ceil(weeks / WEEKS_PER_SEASON)
  week = weeks - ((season - 1) * WEEKS_PER_SEASON)
  return (int(season), int(week))

def get_current_week_season():
  return get_week_season_from_date(datetime.datetime.now())