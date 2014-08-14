// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Custom RemoteArrayMatcher.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.usersuggest.RemoteArrayMatcher');

goog.require('ffc.template.quiz');

goog.require('goog.dom');
goog.require('goog.dom.dataset');
goog.require('goog.events');
goog.require('goog.string');
goog.require('goog.string.path');
goog.require('goog.ui.ac.RemoteArrayMatcher');



/**
 * RemoteArrayMatcher constructor.
 * @constructor
 * @param {string} url The endpoint to the usersuggest service.
 */
ffc.usersuggest.RemoteArrayMatcher = function(url) {
  goog.base(this, url);
};
goog.inherits(ffc.usersuggest.RemoteArrayMatcher,
    goog.ui.ac.RemoteArrayMatcher);


/**
 * @override
 */
ffc.usersuggest.RemoteArrayMatcher.prototype.buildUrl = function(uri, token) {
  return goog.string.path.join(
      uri, ffc.usersuggest.RemoteArrayMatcher.slugify(token));
};

/**
 * Transform text into a URL slug: spaces turned into dashes, remove non alnum
 * @param {string} text The text to slugify.
 * @return {string} The slugified text.
 */
ffc.usersuggest.RemoteArrayMatcher.slugify = function(text) {
  return goog.string.trim(text)
                    .replace(/[^ -a-zA-Z0-9]+/ig, '')
                    .replace(/ /g, '-')
                    .toLowerCase();
};
