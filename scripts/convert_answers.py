#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Batch update film entities."""

import getpass
import logging
import os
import sys
import urllib2
import json

APPENGINE_PATH = '/usr/local/google_appengine/'

def fix_appengine_path():
  EXTRA_PATHS = [
    APPENGINE_PATH,
    os.path.join(APPENGINE_PATH, 'lib', 'antlr3'),
    os.path.join(APPENGINE_PATH, 'lib', 'django'),
    os.path.join(APPENGINE_PATH, 'lib', 'fancy_urllib'),
    os.path.join(APPENGINE_PATH, 'lib', 'ipaddr'),
    os.path.join(APPENGINE_PATH, 'lib', 'webapp2'),
    os.path.join(APPENGINE_PATH, 'lib', 'webob-1.1.1'),
    os.path.join(APPENGINE_PATH, 'lib', 'yaml', 'lib'),
    os.path.join(APPENGINE_PATH, 'lib', 'webapp2-2.5.2'),
  ]
  sys.path.extend(EXTRA_PATHS)

fix_appengine_path()

# Add models to path.
sys.path.insert(0, '/Users/adammcgrath/dev/projects/ffc/src/')

from google.appengine.ext import ndb
from google.appengine.ext.remote_api import remote_api_stub

import models

APP_NAME = 's~ffcapp'
os.environ['AUTH_DOMAIN'] = 'gmail.com'
os.environ['USER_EMAIL'] = 'adamjmcgrath@gmail.com'

ANSWERS = [
  {
    'key': '1989-national-lampoons-christmas-vacation',
    'id': '/en/national_lampoons_christmas_vacation'
  },
  {
    'key': '1992-the-bodyguard',
    'id': '/en/the_bodyguard'
  },
  {
    'key': '1993-groundhog-day',
    'id': '/en/groundhog_day_1993'
  },
  {
    'key': '1993-philadelphia',
    'id': '/en/philadelphia_1993'
  },
  {
    'key': '1991-hook',
    'id': '/en/hook'
  },
  {
    'key': '2010-kickass',
    'id': '/wikipedia/ru_id/1717630'
  },
  {
    'key': '1983-national-lampoons-vacation',
    'id': '/en/national_lampoons_european_vacation'
  },
  {
    'key': '2001-ai-artificial-intelligence',
    'id': '/en/a_i'
  },
  {
    'key': '1987-the-lost-boys',
    'id': '/en/the_lost_boys'
  },
  {
    'key': '2007-atonement',
    'id': '/en/atonement_2007'
  },
  {
    'key': '1986-ferris-buellers-day-off',
    'id': '/en/ferris_buellers_day_off'
  },
]

FAV_FILMS = [
  {
    "fav_film": "Kick-Ass",
    "film_year": 2010,
    "film_title": "Kick-Ass",
    "user": 4546712509087744,
    "film_id": "/wikipedia/ru_id/1717630"
  },
  {
    "fav_film": "The Green Mile",
    "film_year": 1999,
    "film_title": "The Green Mile",
    "user": 4975642303004672,
    "film_id": "/en/the_green_mile_1999"
  },
  {
    "fav_film": "True Romance",
    "film_year": 1993,
    "film_title": "True Romance",
    "user": 5004109346242560,
    "film_id": "/en/true_romance"
  },
  {
    "fav_film": "Grease",
    "film_year": 1978,
    "film_title": "Grease",
    "user": 5020374387392512,
    "film_id": "/en/grease_1978"
  },
  {
    "fav_film": "Garden State",
    "film_year": 2004,
    "film_title": "Garden State",
    "user": 5053703333609472,
    "film_id": "/en/garden_state"
  },
  {
    "fav_film": "The Jungle Book",
    "film_year": 1967,
    "film_title": "The Jungle Book",
    "user": 5207381558427648,
    "film_id": "/en/the_jungle_book_1967"
  },
  {
    "fav_film": "The Lion King",
    "film_year": 1994,
    "film_title": "The Lion King",
    "user": 5226932249559040,
    "film_id": "/en/the_lion_king"
  },
  {
    "fav_film": "In the Name of the Father",
    "film_year": 1993,
    "film_title": "In the Name of the Father",
    "user": 5240452806606848,
    "film_id": "/en/in_the_name_of_the_father"
  },
  {
    "fav_film": "Stealing Beauty",
    "film_year": 1996,
    "film_title": "Stealing Beauty",
    "user": 5257117279715328,
    "film_id": "/en/stealing_beauty"
  },
  {
    "fav_film": "The Shawshank Redemption",
    "film_year": 1994,
    "film_title": "The Shawshank Redemption",
    "user": 5262954140270592,
    "film_id": "/en/the_shawshank_redemption"
  },
  {
    "fav_film": "Heathers",
    "film_year": 1988,
    "film_title": "Heathers",
    "user": 5268894080040960,
    "film_id": "/en/heathers"
  },
  {
    "fav_film": "American Beauty",
    "film_year": 1999,
    "film_title": "American Beauty",
    "user": 5273781752823808,
    "film_id": "/en/american_beauty"
  },
  {
    "fav_film": "Face/Off",
    "film_year": 1997,
    "film_title": "Face/Off",
    "user": 5285584322953216,
    "film_id": "/en/face_off"
  },
  {
    "fav_film": "Eternal Sunshine of the Spotless Mind",
    "film_year": 2004,
    "film_title": "Eternal Sunshine of the Spotless Mind",
    "user": 5301849364103168,
    "film_id": "/en/eternal_sunshine_of_the_spotless_mind"
  },
  {
    "fav_film": "Garden State",
    "film_year": 2004,
    "film_title": "Garden State",
    "user": 5309335492100096,
    "film_id": "/en/garden_state"
  },
  {
    "fav_film": "Goodfellas",
    "film_year": 1990,
    "film_title": "Goodfellas",
    "user": 5314025596387328,
    "film_id": "/en/goodfellas"
  },
  {
    "fav_film": "K-PAX",
    "film_year": 2001,
    "film_title": "K-PAX",
    "user": 5318810189955072,
    "film_id": "/en/k_pax"
  },
  {
    "fav_film": "The Big Lebowski",
    "film_year": 1998,
    "film_title": "The Big Lebowski",
    "user": 5328783104016384,
    "film_id": "/en/the_big_lebowski"
  },
  {
    "fav_film": "The Lord of the Rings: The Two Towers",
    "film_year": 2002,
    "film_title": "The Lord of the Rings: The Two Towers",
    "user": 5340078868004864,
    "film_id": "/en/the_lord_of_the_rings_the_two_towers"
  },
  {
    "fav_film": "True Romance",
    "film_year": 1993,
    "film_title": "True Romance",
    "user": 5521927783317504,
    "film_id": "/en/true_romance"
  },
  {
    "fav_film": "Rocky IV",
    "film_year": 1985,
    "film_title": "Rocky IV",
    "user": 5770331511848960,
    "film_id": "/en/rocky_iv"
  },
  {
    "fav_film": "Sideways",
    "film_year": 2004,
    "film_title": "Sideways",
    "user": 5778586438991872,
    "film_id": "/en/sideways"
  },
  {
    "fav_film": "Ferris Bueller's Day Off",
    "film_year": 1986,
    "film_title": "Ferris Bueller's Day Off",
    "user": 5780068202708992,
    "film_id": "/en/ferris_buellers_day_off"
  },
  {
    "fav_film": "The Shawshank Redemption",
    "film_year": 1994,
    "film_title": "The Shawshank Redemption",
    "user": 5789882202980352,
    "film_id": "/en/the_shawshank_redemption"
  },
  {
    "fav_film": "Groundhog Day",
    "film_year": 1993,
    "film_title": "Groundhog Day",
    "user": 5809329814896640,
    "film_id": "/en/groundhog_day_1993"
  },
  {
    "fav_film": "Star Wars Episode V: The Empire Strikes Back",
    "film_year": 1980,
    "film_title": "Star Wars Episode V: The Empire Strikes Back",
    "user": 5811760766386176,
    "film_id": "/en/star_wars_episode_v_the_empire_strikes_back"
  },
  {
    "fav_film": "The Goonies",
    "film_year": 1985,
    "film_title": "The Goonies",
    "user": 5825904093691904,
    "film_id": "/en/the_goonies"
  },
  {
    "fav_film": "Sliding Doors",
    "film_year": 1998,
    "film_title": "Sliding Doors",
    "user": 5831844033462272,
    "film_id": "/en/sliding_doors"
  },
  {
    "fav_film": "Boogie Nights",
    "film_year": 1997,
    "film_title": "Boogie Nights",
    "user": 5836731706245120,
    "film_id": "/en/boogie_nights"
  },
  {
    "fav_film": "One Flew Over the Cuckoo's Nest",
    "film_year": 1975,
    "film_title": "One Flew Over the Cuckoo's Nest",
    "user": 5844419697704960,
    "film_id": "/en/one_flew_over_the_cuckoos_nest"
  },
  {
    "fav_film": "Babe: Pig in the City",
    "film_year": 1998,
    "film_title": "Babe: Pig in the City",
    "user": 5853396179353600,
    "film_id": "/en/babe_pig_in_the_city"
  },
  {
    "fav_film": "Blade Runner",
    "film_year": 1982,
    "film_title": "Blade Runner",
    "user": 5857961729589248,
    "film_id": "/en/blade_runner"
  },
  {
    "fav_film": "Bowfinger",
    "film_year": 1999,
    "film_title": "Bowfinger",
    "user": 5860723393560576,
    "film_id": "/en/bowfinger"
  },
  {
    "fav_film": "Once Upon a Time in America",
    "film_year": 1984,
    "film_title": "Once Upon a Time in America",
    "user": 5864799317524480,
    "film_id": "/en/once_upon_a_time_in_america"
  },
  {
    "fav_film": "RoboCop",
    "film_year": 1987,
    "film_title": "RoboCop",
    "user": 5869854494031872,
    "film_id": "/en/robocop"
  },
  {
    "fav_film": "Dead Man's Shoes",
    "film_year": 2004,
    "film_title": "Dead Man's Shoes",
    "user": 5876975549808640,
    "film_id": "/en/dead_mans_shoes"
  },
  {
    "fav_film": "Robin Hood: Prince of Thieves",
    "film_year": 1991,
    "film_title": "Robin Hood: Prince of Thieves",
    "user": 5881760143376384,
    "film_id": "/en/robin_hood_prince_of_thieves"
  },
  {
    "fav_film": "One Flew Over the Cuckoo's Nest",
    "film_year": 1975,
    "film_title": "One Flew Over the Cuckoo's Nest",
    "user": 5886725125570560,
    "film_id": "/en/one_flew_over_the_cuckoos_nest"
  },
  {
    "fav_film": "Back to the Future",
    "film_year": 1985,
    "film_title": "Back to the Future",
    "user": 5893640022917120,
    "film_id": "/en/back_to_the_future"
  },
  {
    "fav_film": "Blade Runner",
    "film_year": 1982,
    "film_title": "Blade Runner",
    "user": 5903028821426176,
    "film_id": "/en/blade_runner"
  },
  {
    "fav_film": "The Remains of the Day",
    "film_year": 1993,
    "film_title": "The Remains of the Day",
    "user": 5910046797987840,
    "film_id": "/en/the_remains_of_the_day_1993"
  },
  {
    "fav_film": "The Lord of the Rings: The Return of the King",
    "film_year": 2003,
    "film_title": "The Lord of the Rings: The Return of the King",
    "user": 6084877736738816,
    "film_id": "/en/the_lord_of_the_rings_the_return_of_the_king"
  },
  {
    "fav_film": "Bill & Ted's Excellent Adventure",
    "film_year": 1989,
    "film_title": "Bill &amp; Ted's Excellent Adventure",
    "user": 6130009253085184,
    "film_id": "/en/bill_teds_excellent_adventure"
  },
  {
    "fav_film": "The Usual Suspects",
    "film_year": 1994,
    "film_title": "The Usual Suspects",
    "user": 6333281465270272,
    "film_id": "/en/the_usual_suspects"
  },
  {
    "fav_film": "Hairspray",
    "film_year": 2007,
    "film_title": "Hairspray",
    "user": 6366352713449472,
    "film_id": "/en/hairspray"
  },
  {
    "fav_film": "The Godfather Part II",
    "film_year": 1974,
    "film_title": "The Godfather Part II",
    "user": 6411484229795840,
    "film_id": "/en/the_godfather_part_ii"
  },
  {
    "fav_film": "It's a Mad, Mad, Mad, Mad World",
    "film_year": 1963,
    "film_title": "It's a Mad, Mad, Mad, Mad World",
    "user": 6454683010859008,
    "film_id": "/en/its_a_mad_mad_mad_mad_world"
  },
  {
    "fav_film": "Annie Hall",
    "film_year": 1977,
    "film_title": "Annie Hall",
    "user": 6461078217162752,
    "film_id": "/en/annie_hall"
  },
  {
    "fav_film": "Top Gun",
    "film_year": 1986,
    "film_title": "Top Gun",
    "user": 6692959206506496,
    "film_id": "/en/top_gun"
  }
]



def auth_func():
  return (os.environ['USER_EMAIL'], getpass.getpass('Password:'))


def main():
  # Use 'localhost:8080' for dev server.
  remote_api_stub.ConfigureRemoteDatastore(APP_NAME, '/_ah/remote_api',
      auth_func, servername='ffcapp.appspot.com')

  for a in ANSWERS:
    q = models.Question.query(models.Question.answer == ndb.Key('Film', a['key'], app='s~ffcapp')).get()
    f = urllib2.urlopen('http://films-data.appspot.com/api?id=' + a['id'])
    f_obj = json.load(f)
    q.answer_title = f_obj['title']
    q.answer_year = f_obj['year']
    q.answer_id = f_obj['key']
    print q.put()

  for f in FAV_FILMS:
    u = models.User.get_by_id(f['user'])
    u.favourite_film_title = f['fav_film']
    u.favourite_film_year = f['film_year']
    u.favourite_film_id = f['film_id']
    print u.put()

if __name__ == '__main__':
  main()
