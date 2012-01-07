// @ use_closure_library=true
// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 * 
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.AutoComplete')

goog.require('goog.array')
goog.require('goog.dom')
goog.require('goog.ui.AutoComplete.Renderer')
goog.require('goog.ui.AutoComplete.RichInputHandler')
goog.require('goog.ui.AutoComplete')

goog.require('ffc.RemoteArrayMatcher');



/**
 * AutoComplete constructor.
 * @constructor
 */
ffc.AutoComplete = function(el, elKey) {
  // Create a custom renderer that renders rich rows.  The renderer calls
  // row.render(node, token) for each row.
  var customRenderer = {};
  customRenderer.renderRow = function(row, token, node) {
    return row.data.render(node, token);
  };

  /**
   * A standard renderer that uses a custom row renderer to display the
   * rich rows generated by this autocomplete widget.
   * @type {goog.ui.AutoComplete.Renderer}
   * @private
   */
  var renderer = new goog.ui.AutoComplete.Renderer(null, customRenderer);
  this.renderer_ = renderer;

  var matcher = new ffc.RemoteArrayMatcher(ffc.AutoComplete.API_URL_);
  this.matcher_ = matcher;

  var inputhandler = new goog.ui.AutoComplete.RichInputHandler(null, null,
      false, 300);

  goog.ui.AutoComplete.call(this, matcher, renderer, inputhandler);

  inputhandler.attachAutoComplete(this);
  inputhandler.attachInputs(el);

}
goog.inherits(ffc.AutoComplete, goog.ui.AutoComplete);
goog.exportSymbol('ffc.AutoComplete', ffc.AutoComplete);


/**
 * @private
 */
ffc.AutoComplete.API_URL_ = '/suggest';
// 
// 
// /**
//  * AutoComplete constructor.
//  * @constructor
//  */
// ffc.AutoComplete.prototype.getRowValues = function() {
//   // TODO(adamjmcgrath) Don't use private property of renderer.
//   var rows = this.renderer_.rows_;
//   console.log('rows:');
//   console.log(rows);
//   return goog.array.map(rows, function(r) {return r.data['title']});
// };