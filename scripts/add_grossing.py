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
    help='Location of the films CSV.')

parser.add_option('-g', '--grossing', dest='grossing',
    help='Location of the grossing figures CSV.')

parser.add_option('-o', '--output', dest='output',
    help='Location of the CSV to output.')

opts, args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)


def tokenize(string):
  return re.sub(r'[^\w\d]+', '', string.split('(')[0].strip()).lower()

def main():
  if opts.films is None or opts.grossing is None or opts.output is None:
      print 'Missing arguments.'
      parser.print_help()
      exit(-1)

  output_csv_file = open(opts.output, 'wb')
  output_csv_writer = csv.writer(output_csv_file)

  grossing_csv_file = open(opts.grossing, 'rb')
  grossing_csv_reader = csv.reader(grossing_csv_file)

  films_csv_file = open(opts.films, 'rb')
  films_csv_reader = csv.reader(films_csv_file)

  grossing_dict = {}
  for grossing_row in grossing_csv_reader:
    token = tokenize(grossing_row[1])
    grossing_dict[token] = grossing_row[2]

  found = 0
  not_found = 0
  for film_row in films_csv_reader:
      film_title = film_row[1]
      try:
        film_row.append(grossing_dict[tokenize(film_title)])
        found += 1
      except KeyError:
        not_found += 1
      output_csv_writer.writerow(film_row)

  logging.info('Found: %d' % found)
  logging.info('Not found: %d' % not_found)

  films_csv_file.close()
  grossing_csv_file.close()
  output_csv_file.close()


if __name__ == '__main__':
  main()
