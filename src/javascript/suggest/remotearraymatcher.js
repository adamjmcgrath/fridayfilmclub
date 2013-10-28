// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Custom RemoteArrayMatcher.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.suggest.RemoteArrayMatcher');

goog.require('ffc.template.quiz');

goog.require('goog.dom');
goog.require('goog.dom.dataset');
goog.require('goog.events');
goog.require('goog.string.path');
goog.require('goog.ui.ac.RemoteArrayMatcher');



/**
 * RemoteArrayMatcher constructor.
 * @constructor
 * @param {string} url The endpoint to the suggest service.
 * @param {string} fieldName
 */
ffc.suggest.RemoteArrayMatcher = function(url, fieldName) {
  goog.base(this, url);

  this.fieldName = fieldName;
};
goog.inherits(ffc.suggest.RemoteArrayMatcher,
    goog.ui.ac.RemoteArrayMatcher);


/**
 * @override
 */
ffc.suggest.RemoteArrayMatcher.prototype.buildUrl = function(uri, token) {
  return goog.string.path.join(
      uri, ffc.suggest.RemoteArrayMatcher.slugify(token));
};


/**
 * @override
 */
ffc.suggest.RemoteArrayMatcher.prototype.requestMatchingRows =
    function(token, maxMatches, matchHandler) {
  // Augment the matchhandler to add/update the render/select row methods.
  var myMatchHandler = goog.bind(this.augmentMatchHandler, this, matchHandler);

  goog.base(this, 'requestMatchingRows', token, maxMatches, myMatchHandler);
};


/**
 * @override
 */
ffc.suggest.RemoteArrayMatcher.prototype.augmentMatchHandler =
    function(matchHandler, token, matches) {
  var rows = [];
  for (var i = 0; i < matches.length; i++) {
    var row = matches[i];
    row.render = goog.bind(
        ffc.suggest.RemoteArrayMatcher.rowRender, this, row, i);
    row.select = goog.bind(ffc.suggest.RemoteArrayMatcher.rowSelect, this, row);
    rows.push(row);
  }
  if (this.rowFilter_) {
    rows = this.rowFilter_(rows);
  }
  matchHandler(token, rows);
};


/**
 * Render a row.
 * @param {Object} newRow The new row.
 * @param {number} pos The index of the row.
 * @param {Element} node The element in which to render the row.
 */
ffc.suggest.RemoteArrayMatcher.rowRender = function(newRow, pos, node) {
  soy.renderElement(node, ffc.template.quiz.option, {
    title: newRow['title'],
    key: newRow['key'],
    year: newRow['year'],
    odd: (pos % 2) != 0,
    fieldName: this.fieldName
  });
};


/**
 * @override
 */
ffc.suggest.RemoteArrayMatcher.rowSelect = function(newRow, target) {
  target.value = newRow['title'];
};


/**
 * Transform text into a URL slug: spaces turned into dashes, remove non alnum
 * @param {string} text The text to slugify.
 * @return {string} The slugified text.
 */
ffc.suggest.RemoteArrayMatcher.slugify = function(text) {
  return (text.replace(/[^-a-zA-Z0-9]+/ig, '')).toLowerCase();
};
