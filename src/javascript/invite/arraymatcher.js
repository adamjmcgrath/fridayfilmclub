// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Custom ArrayMatcher.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.invite.ArrayMatcher');

goog.require('goog.dom');
goog.require('goog.dom.dataset');
goog.require('goog.events');
goog.require('goog.string');
goog.require('goog.string.path');
goog.require('goog.ui.ac.ArrayMatcher');



/**
 * ArrayMatcher constructor.
 * @constructor
 */
ffc.invite.ArrayMatcher = function() {
  goog.base(this);
};
goog.inherits(ffc.invite.ArrayMatcher, goog.ui.ac.ArrayMatcher);


/**
 * @override
 */
ffc.invite.ArrayMatcher.prototype.requestMatchingRows =
    function(token, maxMatches, matchHandler) {
  // Augment the matchhandler to add/update the render/select row methods.
  var myMatchHandler = goog.bind(this.augmentMatchHandler, this, matchHandler);

  goog.base(this, 'requestMatchingRows', token, maxMatches, myMatchHandler);
};


/**
 * @override
 */
ffc.invite.ArrayMatcher.prototype.augmentMatchHandler =
    function(matchHandler, token, matches) {
  var rows = [];
  for (var i = 0; i < matches.length; i++) {
    var row = matches[i];
    row.render = goog.bind(
        ffc.invite.ArrayMatcher.rowRender, this, row, i);
    row.select = goog.bind(ffc.invite.ArrayMatcher.rowSelect, this, row);
    row.toString = goog.bind(ffc.invite.ArrayMatcher.rowToString, this, row);
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
 * @this {ffc.invite.ArrayMatcher}
 */
ffc.invite.ArrayMatcher.rowRender = function(newRow, pos, node) {
  var p = document.createElement('p');
  p.innerHTML = newRow['title'];
  node.appendChild(p);
};


/**
 * @override
 */
ffc.invite.ArrayMatcher.rowSelect = function(newRow, target) {
  target.value = '';
  var newNode = document.createElement('span');
  newNode.innerHTML = newRow['title'];
  goog.dom.insertSiblingBefore(newNode, target);
};


/**
 * @override
 */
ffc.invite.ArrayMatcher.rowToString = function(newRow) {
  return '';
};


/**
 * Transform text into a URL slug: spaces turned into dashes, remove non alnum
 * @param {string} text The text to slugify.
 * @return {string} The slugified text.
 */
ffc.invite.ArrayMatcher.slugify = function(text) {
  return goog.string.trim(text)
                    .replace(/[^ -a-zA-Z0-9]+/ig, '')
                    .replace(/ /g, '-')
                    .toLowerCase();
};
