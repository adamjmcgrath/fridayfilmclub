// @ use_closure_library=true
// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.suggest.AutoComplete');

goog.require('ffc.suggest.RemoteArrayMatcher');

goog.require('goog.array');
goog.require('goog.dom');
goog.require('goog.ui.AutoComplete');
goog.require('goog.ui.AutoComplete.Renderer');
goog.require('goog.ui.AutoComplete.RichInputHandler');



/**
 * AutoComplete constructor.
 * @param {HTMLInputElement} el The input element to decorate.
 * @param {Element} parent The element to render the autocomplete in.
 * @constructor
 */
ffc.suggest.AutoComplete = function(el, parent) {
  // Create a custom renderer that renders rich rows.
  // The renderer calls row.render(node, token) for each row.
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
  this.renderer_ = new goog.ui.AutoComplete.Renderer(parent, customRenderer);

  /**
   * A matcher the takes a uri to a suggest endpoint and returns an object to
   * use in the renderer.
   * @type {ffc.suggest.RemoteArrayMatcher}
   * @private
   */
  this.matcher_ = new ffc.suggest.RemoteArrayMatcher(
      ffc.suggest.AutoComplete.API_URL_);

  var inputhandler = new goog.ui.AutoComplete.RichInputHandler(
      null, null, false, 300);
  inputhandler.handleBlur = function() {};

  goog.ui.AutoComplete.call(this, this.matcher_, this.renderer_, inputhandler);

  inputhandler.attachAutoComplete(this);
  inputhandler.attachInputs(el);
};
goog.inherits(ffc.suggest.AutoComplete, goog.ui.AutoComplete);
goog.exportSymbol('ffc.suggest.AutoComplete', ffc.suggest.AutoComplete);


/**
 * @type {string}
 * @private
 */
ffc.suggest.AutoComplete.API_URL_ = '/suggest';


/**
 * @override
 * @param {boolean} reallyDismiss only fire the autcomplete dismiss in
 *     certain circumstances.
 */
ffc.suggest.AutoComplete.prototype.dismiss = function(reallyDismiss) {
  if (reallyDismiss) {
    goog.base(this, 'dismiss');
  }
};
