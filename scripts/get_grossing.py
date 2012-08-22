#!/usr/bin/env python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Scrapes Box Office Mojo, adds grossing data to films CSV."""

import csv
import datetime
import logging
from optparse import OptionParser
import urllib2
import re

from bs4 import BeautifulSoup

parser = OptionParser() 

parser.add_option('-s', '--start_year', type='int', default=1980,
    help='The start year for scraping films (boxofficemojo goes back to 1980).')

parser.add_option('-e', '--end_year', type='int',
    default=datetime.datetime.now().year,
    help='The end year for scraping films.')

parser.add_option('-f', '--output', dest='output',
    help='Location of the output csv')

opts, args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)

URL = 'http://boxofficemojo.com/yearly/chart/?yr=%s&page=%s'
NUMBER_RE = r'[^0-9\.]'


def main():
  if opts.output is None:
      print 'Missing --ouput argument.'
      parser.print_help()
      exit(-1)
  csv_file = open(opts.output, 'wb')
  csv_writer = csv.writer(csv_file)

  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]

  for y in range(opts.start_year, opts.end_year + 1):
    logging.info('Scraping year: %d', y)
    page_counter = 0
    next_year = True
    while next_year:
      page_counter += 1
      url = URL % (y, page_counter)
      soup = BeautifulSoup(opener.open(url).read(), 'lxml')
      try:
        table = soup.select('div#body table table table')[1]
      except IndexError:
        # No table of films, we've gone past the last page. Move to next year.
        next_year = False
        continue
      row_counter = 0
      for tr in table.select('tr'):
        row_counter += 1
        if row_counter < 3:
          continue
        tds = tr.select('td')
        try:
          title = tds[1].get_text()
        except IndexError:
          # Unexpected row of td's.
          continue
        try:
          grossing = int(re.sub(NUMBER_RE, '', tds[3].get_text()))
        except ValueError:
          # Invalid grossing figure.
          continue
      
        csv_writer.writerow([y, title.encode('utf8'), grossing])

  csv_file.close()


if __name__ == '__main__':
  main()
