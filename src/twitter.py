#!/usr/bin/python

"""Create Twitter Oauth header."""

import random
import string
import time
import urllib
from urlparse import urlparse

import hmac
import hashlib

import secrets


consumer_token, consumer_token_secret = secrets.AUTH_CONFIG['twitter']


def timestamp():
  return int(round(time.time()))


def generate_nonce():
  nonce = ''.join(random.choice(string.ascii_uppercase +
                  string.ascii_lowercase + string.digits) for x in range(32))
  return nonce


def signature_base_for_request(url, params, method):
  param_string = ''

  sorted_keys = sorted(params.iterkeys())
  for key in sorted_keys:
    s = key + '=' + params[key]
    if param_string.__len__() > 0:
      param_string += '&' + s
    else:
      param_string = s

  params = urllib.quote_plus(param_string)

  url = urlparse(url)
  url = 'https://api.twitter.com' + url.path
  url = urllib.quote_plus(url)

  method = method.upper()
  signature_base = method + '&' + url + '&' + params
  return signature_base


def signing_key(access_token_secret):
  return consumer_token_secret + '&' + access_token_secret


def sign_signature(signature_base, sign_key):
  digest = hmac.new(sign_key, signature_base, hashlib.sha1).digest()

  signature = digest.encode('base64','strict')
  signature = signature[:-1]  # remove newline

  return signature


def signature_for_request(url, params, method, access_token_secret):
  signature_base = signature_base_for_request(url, params, method)
  signature = sign_signature(signature_base, signing_key(access_token_secret))

  return signature


def header_dictionary_without_signature(access_token):
  return {
      'oauth_consumer_key': consumer_token,
      'oauth_nonce': generate_nonce(),
      'oauth_signature_method': 'HMAC-SHA1',
      'oauth_timestamp': str(timestamp()),
      'oauth_token': access_token,
      'oauth_version': '1.0',
  }


def header_string_for_request(url, params, method, access_token,
                              access_token_secret):
  headers = header_dictionary_without_signature(access_token)

  for key in headers.iterkeys():
    params[key] = headers[key]

  headers['oauth_signature'] = signature_for_request(url, params,
                                                     method,
                                                     access_token_secret)
  headers_keys = sorted(headers.iterkeys())

  header_string = 'OAuth '

  for key in headers_keys:
    value = headers[key]
    header_string += (urllib.quote_plus(key) + '="' +
                      urllib.quote_plus(value) + '", ')

  header_string = header_string[:-2]  # remove the ', '
  return header_string
