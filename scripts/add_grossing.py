#!/usr/bin/env python
#
# Copyright 2011 Friday Film Club. All Rights Reserved.

"""Add grossing figures to film data."""

import csv
import datetime
import logging
from optparse import OptionParser
import re

from bs4 import BeautifulSoup

parser = OptionParser() 


parser.add_option('-f', '--films', dest='films',
    help='Location of the films csv')

parser.add_option('-g', '--grossing', dest='grossing',
    help='Location of the grossing figures csv')

opts, args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)



def main():
  if opts.films is None or opts.grossing is None:
      print 'Missing films or grossing csv\'s argument.'
      parser.print_help()
      exit(-1)

  grossing_csv_file = open(opts.grossing, 'rb')
  grossing_csv_reader = csv.reader(grossing_csv_file)

  films_csv_file = open(opts.films, 'rb')
  films_csv_reader = csv.reader(films_csv_file)

  grossing_dict = {}
  for grossing_row in grossing_csv_reader:
    grossing_dict[grossing_row[1].split('(')[0].strip()] = grossing_row[2]

  found = 0
  not_found = 0
  for film_row in films_csv_reader:
      film_title = film_row[1]
      try:
        grossing_dict[film_title]
        found += 1
      except KeyError:
        not_found += 1
        # if int(film_row[0]) > 1990:
        print film_title

  print 'found: %d' % found
  print 'not_found: %d' % not_found

  films_csv_file.close()
  grossing_csv_file.close()


if __name__ == '__main__':
  main()
