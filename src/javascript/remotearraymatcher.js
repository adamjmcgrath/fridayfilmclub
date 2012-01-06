// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Remote array matcher.
 * 
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.RemoteArrayMatcher');

goog.require('goog.events');
goog.require('goog.dom');
goog.require('goog.dom.dataset');
goog.require('goog.ui.AutoComplete.RemoteArrayMatcher');
goog.require('goog.string.path');



/**
 * @constructor
 */
ffc.RemoteArrayMatcher = function(url, keyEl) {
  goog.base(this, url);
};
goog.inherits(ffc.RemoteArrayMatcher,
    goog.ui.AutoComplete.RemoteArrayMatcher);


/**
 * @override
 */
ffc.RemoteArrayMatcher.prototype.buildUrl = function(uri, token) {
  return goog.string.path.join(uri, ffc.RemoteArrayMatcher.slugify(token));
};


/**
 * @override
 */
ffc.RemoteArrayMatcher.prototype.requestMatchingRows =
    function(token, maxMatches, matchHandler) {
  // Augment the matchhandler to add/update the render/select row methods.
  var myMatchHandler = goog.bind(this.augmentMatchHandler, this, matchHandler);

  goog.base(this, 'requestMatchingRows', token, maxMatches, myMatchHandler);
};


/**
 * @override
 */
ffc.RemoteArrayMatcher.prototype.augmentMatchHandler =
    function(matchHandler, token, matches) {
  var rows = [];
  for (var i = 0; i < matches.length; i++) {
    var row = matches[i];
    row.render = goog.bind(ffc.RemoteArrayMatcher.rowRender, this, row);
    row.select = goog.bind(ffc.RemoteArrayMatcher.rowSelect, this, row);
    rows.push(row);
  }
  if (this.rowFilter_) {
    rows = this.rowFilter_(rows);
  }
  matchHandler(token, rows);
};


/**
 *
 */
ffc.RemoteArrayMatcher.rowRender = function(newRow, node, token) {
  node.innerHTML = newRow['title'] + ' <span>' + newRow['year'] + '</span>';
};


/**
 *
 */
ffc.RemoteArrayMatcher.rowSelect = function(newRow, target) {
  target.value = newRow['title'];
};


/**
 * Transform text into a URL slug: spaces turned into dashes, remove non alnum
 * @param string text
 */
ffc.RemoteArrayMatcher.slugify = function(text) {
  return (text.replace(/[^-a-zA-Z0-9]+/ig, '')).toLowerCase();
};
