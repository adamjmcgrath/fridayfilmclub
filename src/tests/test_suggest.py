#!/usr/bin/python
#
# Copyright Friday Film Club. All Rights Reserved.

"""Suggest unit tests."""


__author__ = 'adamjmcgrath@gmail.com (Adam McGrath)'

import unittest

import base


class SuggestTestCase(base.TestCase):

  def test_suggest_blank(self):
    response = self.get('/suggest/%20')
    self.assertEqual(response.body, '')

  def test_suggest_film(self):
    response = self.get_json('/suggest/top-gun')
    self.assertIn('Top Gun', [film['title'] for film in response])


if __name__ == '__main__':
    unittest.main()
