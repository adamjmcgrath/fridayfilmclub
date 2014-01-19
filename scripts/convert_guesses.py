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

GUESSES = [
  {
    "new_title": "American Beauty",
    "new_key": "/en/american_beauty",
    "new_year": 1999,
    "original_title": "American Beauty",
    "original_year": 1999
  },
  {
    "new_title": "A Christmas Carol",
    "new_key": "/wikipedia/en_title/A_Christmas_Carol_$00281997_film$0029",
    "new_year": 1997,
    "original_title": "A Christmas Carol",
    "original_year": 1997
  },
  {
    "new_title": "Heathers",
    "new_key": "/en/heathers",
    "new_year": 1988,
    "original_title": "Heathers",
    "original_year": 1989
  },
  {
    "new_title": "How the Grinch Stole Christmas",
    "new_key": "/en/how_the_grinch_stole_christmas",
    "new_year": 2000,
    "original_title": "How the Grinch Stole Christmas",
    "original_year": 2000
  },
  {
    "new_title": "Basic Instinct",
    "new_key": "/en/basic_instinct",
    "new_year": 1992,
    "original_title": "Basic Instinct",
    "original_year": 1992
  },
  {
    "new_title": "Garden State",
    "new_key": "/en/garden_state",
    "new_year": 2004,
    "original_title": "Garden State",
    "original_year": 2004
  },
  {
    "new_title": "When Harry Met Sally...",
    "new_key": "/en/when_harry_met_sally",
    "new_year": 1989,
    "original_title": "When Harry Met Sally...",
    "original_year": 1989
  },
  {
    "new_title": "The Shining",
    "new_key": "/en/the_shining",
    "new_year": 1980,
    "original_title": "The Shining",
    "original_year": 1980
  },
  {
    "new_title": "The Sixth Sense",
    "new_key": "/en/the_sixth_sense",
    "new_year": 1999,
    "original_title": "The Sixth Sense",
    "original_year": 1999
  },
  {
    "new_title": "The Breakfast Club",
    "new_key": "/en/the_breakfast_club",
    "new_year": 1985,
    "original_title": "The Breakfast Club",
    "original_year": 1985
  },
  {
    "new_title": "Kiss Kiss Bang Bang",
    "new_key": "/en/kiss_kiss_bang_bang",
    "new_year": 2005,
    "original_title": "Kiss Kiss Bang Bang",
    "original_year": 2005
  },
  {
    "new_title": "Bad Santa",
    "new_key": "/en/bad_santa",
    "new_year": 2003,
    "original_title": "Bad Santa",
    "original_year": 2003
  },
  {
    "new_title": "National Lampoon's Vacation",
    "new_key": "/en/national_lampoons_european_vacation",
    "new_year": 1985,
    "original_title": "National Lampoon's Vacation",
    "original_year": 1983
  },
  {
    "new_title": "Cocktail",
    "new_key": "/en/cocktail_1989",
    "new_year": 1988,
    "original_title": "Cocktail",
    "original_year": 1988
  },
  {
    "new_title": "Atonement",
    "new_key": "/en/atonement_2007",
    "new_year": 2007,
    "original_title": "Atonement",
    "original_year": 2007
  },
  {
    "new_title": "The Mummy Returns",
    "new_key": "/en/the_mummy_returns",
    "new_year": 2001,
    "original_title": "The Mummy Returns",
    "original_year": 2001
  },
  {
    "new_title": "National Lampoon's TV: The Movie",
    "new_key": "/en/national_lampoons_tv_the_movie",
    "new_year": 2006,
    "original_title": "National Lampoon's TV: The Movie",
    "original_year": 2007
  },
  {
    "new_title": "Magnolia",
    "new_key": "/en/magnolia_2000",
    "new_year": 1999,
    "original_title": "Magnolia",
    "original_year": 1999
  },
  {
    "new_title": "The Matrix",
    "new_key": "/en/the_matrix",
    "new_year": 1999,
    "original_title": "The Matrix",
    "original_year": 1999
  },
  {
    "new_title": "On the Road",
    "new_key": "/en/in_search_of_on_the_road_a_work_in_progress",
    "new_year": 2012,
    "original_title": "On the Road",
    "original_year": 2012
  },
  {
    "new_title": "Black Swan",
    "new_key": "/wikipedia/fr/Black_Swan_$0028film$0029",
    "new_year": 2010,
    "original_title": "Black Swan",
    "original_year": 2010
  },
  {
    "new_title": "She's All That",
    "new_key": "/en/shes_all_that",
    "new_year": 1999,
    "original_title": "She's All That",
    "original_year": 1999
  },
  {
    "new_title": "Revenge of the Nerds",
    "new_key": "/en/revenge_of_the_nerds",
    "new_year": 1984,
    "original_title": "Revenge of the Nerds",
    "original_year": 1984
  },
  {
    "new_title": "Days of Thunder",
    "new_key": "/en/days_of_thunder",
    "new_year": 1990,
    "original_title": "Days of Thunder",
    "original_year": 1990
  },
  {
    "new_title": "The 6th Day",
    "new_key": "/en/the_6th_day",
    "new_year": 2000,
    "original_title": "The 6th Day",
    "original_year": 2000
  },
  {
    "new_title": "Paris, je t'aime",
    "new_key": "/en/paris_je_taime",
    "new_year": 2006,
    "original_title": "Paris, je t'aime",
    "original_year": 2006
  },
  {
    "new_title": "The Family Man",
    "new_key": "/en/the_family_man",
    "new_year": 2000,
    "original_title": "The Family Man",
    "original_year": 2000
  },
  {
    "new_title": "Terminator 2: Judgment Day",
    "new_key": "/en/terminator_2_judgment_day",
    "new_year": 1991,
    "original_title": "Terminator 2: Judgment Day",
    "original_year": 1991
  },
  {
    "new_title": "Top Gun",
    "new_key": "/en/top_gun",
    "new_year": 1986,
    "original_title": "Top Gun",
    "original_year": 1986
  },
  {
    "new_title": "The Talented Mr. Ripley",
    "new_key": "/en/the_talented_mr_ripley_1999",
    "new_year": 1999,
    "original_title": "The Talented Mr. Ripley",
    "original_year": 1999
  },
  {
    "new_title": "Bad Teacher",
    "new_key": "/en/bad_teacher",
    "new_year": 2011,
    "original_title": "Bad Teacher",
    "original_year": 2011
  },
  {
    "new_title": "Boogie Nights",
    "new_key": "/en/boogie_nights",
    "new_year": 1997,
    "original_title": "Boogie Nights",
    "original_year": 1997
  },
  {
    "new_title": "Evita",
    "new_key": "/en/evita_1996",
    "new_year": 1996,
    "original_title": "Evita",
    "original_year": 1996
  },
  {
    "new_title": "A.I. Artificial Intelligence",
    "new_key": "/en/a_i",
    "new_year": 2001,
    "original_title": "A.I. Artificial Intelligence",
    "original_year": 2001
  },
  {
    "new_title": "Dirty Dancing",
    "new_key": "/en/dirty_dancing",
    "new_year": 1987,
    "original_title": "Dirty Dancing",
    "original_year": 1987
  },
  {
    "new_title": "The Bodyguard 2",
    "new_key": "/en/the_bodyguard_2",
    "new_year": 2007,
    "original_title": "The Bodyguard 2",
    "original_year": 2007
  },
  {
    "new_title": "Signs",
    "new_key": "/en/signs",
    "new_year": 2002,
    "original_title": "Signs",
    "original_year": 2002
  },
  {
    "new_title": "Fast Times at Ridgemont High",
    "new_key": "/en/fast_times_at_ridgemont_high",
    "new_year": 1982,
    "original_title": "Fast Times at Ridgemont High",
    "original_year": 1982
  },
  {
    "new_title": "National Lampoon's Christmas Vacation",
    "new_key": "/en/national_lampoons_christmas_vacation",
    "new_year": 1989,
    "original_title": "National Lampoon's Christmas Vacation",
    "original_year": 1989
  },
  {
    "new_title": "The Graduate",
    "new_key": "/en/the_graduate",
    "new_year": 1967,
    "original_title": "The Graduate",
    "original_year": 1967
  },
  {
    "new_title": "10 Things I Hate About You",
    "new_key": "/en/10_things_i_hate_about_you",
    "new_year": 1999,
    "original_title": "10 Things I Hate About You",
    "original_year": 1999
  },
  {
    "new_title": "The Bodyguard",
    "new_key": "/en/the_bodyguard",
    "new_year": 1992,
    "original_title": "The Bodyguard",
    "original_year": 1992
  },
  {
    "new_title": "A Very Harold & Kumar 3D Christmas",
    "new_key": "/wikipedia/en_title/A_Very_Harold_$0026_Kumar_3D_Christmas",
    "new_year": 2011,
    "original_title": "A Very Harold & Kumar 3D Christmas",
    "original_year": 2011
  },
  {
    "new_title": "Four Christmases",
    "new_key": "/en/four_christmases",
    "new_year": 2008,
    "original_title": "Four Christmases",
    "original_year": 2008
  },
  {
    "new_title": "Love Actually",
    "new_key": "/en/love_actually",
    "new_year": 2003,
    "original_title": "Love Actually",
    "original_year": 2003
  },
  {
    "new_title": "Hot Shots!",
    "new_key": "/en/hot_shots",
    "new_year": 1991,
    "original_title": "Hot Shots!",
    "original_year": 1991
  },
  {
    "new_title": "Election",
    "new_key": "/en/election_2005",
    "new_year": 2005,
    "original_title": "Election",
    "original_year": 2005
  },
  {
    "new_title": "How I Got into College",
    "new_key": "/en/how_i_got_into_college",
    "new_year": 1989,
    "original_title": "How I Got into College",
    "original_year": 1989
  },
  {
    "new_title": "The Big Lebowski",
    "new_key": "/en/the_big_lebowski",
    "new_year": 1998,
    "original_title": "The Big Lebowski",
    "original_year": 1998
  },
  {
    "new_title": "Boyz n the Hood",
    "new_key": "/en/boyz_n_the_hood",
    "new_year": 1991,
    "original_title": "Boyz n the Hood",
    "original_year": 1991
  },
  {
    "new_title": "Rambo III",
    "new_key": "/en/rambo_iii",
    "new_year": 1988,
    "original_title": "Rambo III",
    "original_year": 1988
  },
  {
    "new_title": "M",
    "new_key": "/wikipedia/en_title/The_Other_Side_$00282011_film$0029",
    "new_year": 2013,
    "original_title": "M",
    "original_year": 2007
  },
  {
    "new_title": "Babe: Pig in the City",
    "new_key": "/en/babe_pig_in_the_city",
    "new_year": 1998,
    "original_title": "Babe",
    "original_year": 1995
  },
  {
    "new_title": "Ten",
    "new_key": "/en/ten_2002",
    "new_year": 2002,
    "original_title": "Ten",
    "original_year": 2002
  },
  {
    "new_title": "The Crying Game",
    "new_key": "/en/the_crying_game",
    "new_year": 1992,
    "original_title": "The Crying Game",
    "original_year": 1992
  },
  {
    "new_title": "Wind",
    "new_key": "/en/wind_1992",
    "new_year": 1992,
    "original_title": "Wind",
    "original_year": 1992
  },
  {
    "new_title": "American Pie",
    "new_key": "/en/american_pie_1999",
    "new_year": 1999,
    "original_title": "American Pie",
    "original_year": 1999
  },
  {
    "new_title": "Ferris Bueller's Day Off",
    "new_key": "/en/ferris_buellers_day_off",
    "new_year": 1986,
    "original_title": "Ferris Bueller's Day Off",
    "original_year": 1986
  },
  {
    "new_title": "Love Story",
    "new_key": "/en/love_story_1981",
    "new_year": 1981,
    "original_title": "Love Story",
    "original_year": 1981
  },
  {
    "new_title": "Dances with Wolves",
    "new_key": "/en/dances_with_wolves",
    "new_year": 1990,
    "original_title": "Dances with Wolves",
    "original_year": 1990
  },
  {
    "new_title": "Forrest Gump",
    "new_key": "/en/forrest_gump",
    "new_year": 1994,
    "original_title": "Forrest Gump",
    "original_year": 1994
  },
  {
    "new_title": "Sleepless in Seattle",
    "new_key": "/en/sleepless_in_seattle",
    "new_year": 1993,
    "original_title": "Sleepless in Seattle",
    "original_year": 1993
  },
  {
    "new_title": "Jerry Maguire",
    "new_key": "/en/jerry_maguire",
    "new_year": 1996,
    "original_title": "Jerry Maguire",
    "original_year": 1996
  },
  {
    "new_title": "Pretty Woman",
    "new_key": "/en/pretty_woman",
    "new_year": 1990,
    "original_title": "Pretty Woman",
    "original_year": 1990
  },
  {
    "new_title": "Wimbledon",
    "new_key": "/en/wimbledon_2004",
    "new_year": 2004,
    "original_title": "Wimbledon",
    "original_year": 2004
  },
  {
    "new_title": "Elf",
    "new_key": "/en/elf_2003",
    "new_year": 2003,
    "original_title": "Elf",
    "original_year": 2003
  },
  {
    "new_title": "Planes, Trains and Automobiles",
    "new_key": "/en/planes_trains_and_automobiles",
    "new_year": 1987,
    "original_title": "Planes, Trains and Automobiles",
    "original_year": 1987
  },
  {
    "new_title": "Bull Durham",
    "new_key": "/en/bull_durham",
    "new_year": 1988,
    "original_title": "Bull Durham",
    "original_year": 1988
  },
  {
    "new_title": "Coming to America",
    "new_key": "/en/coming_to_america",
    "new_year": 1988,
    "original_title": "Coming to America",
    "original_year": 1988
  },
  {
    "new_title": "You've Got Mail",
    "new_key": "/en/youve_got_mail",
    "new_year": 1998,
    "original_title": "You've Got Mail",
    "original_year": 1998
  },
  {
    "new_title": "Johnson Family Vacation",
    "new_key": "/en/johnson_family_vacation",
    "new_year": 2004,
    "original_title": "Johnson Family Vacation",
    "original_year": 2004
  },
  {
    "new_title": "Pay It Forward",
    "new_key": "/en/pay_it_forward",
    "new_year": 2000,
    "original_title": "Pay It Forward",
    "original_year": 2000
  },
  {
    "new_title": "The Others",
    "new_key": "/en/the_others_2001",
    "new_year": 2001,
    "original_title": "The Others",
    "original_year": 2001
  },
  {
    "new_title": "The Notebook",
    "new_key": "/wikipedia/pl/Pami$0119tnik_$0028film$0029",
    "new_year": 2004,
    "original_title": "The Notebook",
    "original_year": 2004
  },
  {
    "new_title": "Shipwrecked",
    "new_key": "/en/shipwrecked",
    "new_year": 1990,
    "original_title": "Shipwrecked",
    "original_year": 1990
  },
  {
    "new_title": "Seeking a Friend for the End of the World",
    "new_key": "/wikipedia/en_title/Seeking_a_Friend_for_the_End_of_the_World",
    "new_year": 2012,
    "original_title": "Seeking a Friend for the End of the World",
    "original_year": 2012
  },
  {
    "new_title": "Say Anything...",
    "new_key": "/en/say_anything",
    "new_year": 1989,
    "original_title": "Say Anything...",
    "original_year": 1989
  }
]


def auth_func():
  return (os.environ['USER_EMAIL'], getpass.getpass('Password:'))


def get_guess_by_old_title(old_title):
  for g in GUESSES:
    if g["original_title"] == old_title:
      return g
  return None


def main():
  # Use 'localhost:8080' for dev server.
  remote_api_stub.ConfigureRemoteDatastore(APP_NAME, '/_ah/remote_api',
      auth_func, servername='ffcapp.appspot.com')

  for uq in models.UserQuestion.query():
    new_guesses = []
    for g in uq.guesses:
      if g != 'pass':
        film = models.Film.get_by_id(g)
        if not film:
          print 'New: ' + g
        else:
          film_obj = get_guess_by_old_title(film.title)
          if film_obj:
            g = film_obj['new_key']
          else:
            g = 'pass'
      new_guesses.append(g)

    uq.guesses = new_guesses
    print uq.put()






if __name__ == '__main__':
  main()
