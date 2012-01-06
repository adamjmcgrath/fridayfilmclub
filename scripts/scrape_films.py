#!/usr/bin/env python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Scrapes Wikipedia for film titles, outputs year and title into a CSV."""

import csv
import datetime
import logging
from optparse import OptionParser
import urllib2
import re

from third_party.BeautifulSoup import BeautifulSoup

parser = OptionParser() 

parser.add_option('-s', '--start_year', type='int', default=1900,
    help='The start year for scraping films.')

parser.add_option('-e', '--end_year', type='int',
    default=datetime.datetime.now().year,
    help='The end year for scraping films.')

parser.add_option('-o', '--output', dest='output',
    help='Location to output CSV file')

opts, args = parser.parse_args()

WIKI_HOST = 'http://en.wikipedia.org'
WIKI_URL = WIKI_HOST + '/wiki/Category:%d_movies'
FILM_RE = re.compile(r' *\(.*movie\)')
FILM_FILE = 'films.csv'


def get_films_from_page(opener, csv_writer, y, url, film_list):
  infile = opener.open(url)
  response = infile.read()
  soup = BeautifulSoup(response)
  films = soup.find('div', {'class':  'mw-content-ltr'});
  for link in films.findAll('a'):
    try:
      title = link['title']
      if not (title.startswith('Category:') or
              title.startswith('Wikipedia:') or
              title.endswith('in movie')):
        film_title = re.sub(FILM_RE, '', title)
        csv_writer.writerow([y, film_title.encode('utf8')])
    except KeyError:
      pass
  print '  next page'
  try:
    next_url = WIKI_HOST + soup.find('a', text='next 200').parent['href']
    get_films_from_page(opener, csv_writer, y, next_url, film_list)
  except (KeyError, AttributeError):
    pass


def main():
  if opts.output is None:
      print 'Missing --file argument.'
      parser.print_help()
      exit(-1)
  csv_file = open(opts.output, 'wb')
  csv_writer = csv.writer(csv_file)

  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]

  film_list = set()
  for y in range(opts.start_year, opt.end_year + 1):
    logging.info('Scraping year: %d', y)
    url = WIKI_URL % y
    get_films_from_page(opener, csv_writer, y, url, film_list)


if __name__ == '__main__':
  main()
