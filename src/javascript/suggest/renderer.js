// @ use_closure_library=true
// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 * 
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.AutoCompleteRenderer')

goog.require('goog.ui.AutoComplete.Renderer')



/**
 * AutoComplete constructor.
 * @constructor
 */
ffc.AutoCompleteRenderer = function(parent, customRenderer) {
  goog.base(this, parent, customRenderer);
}
goog.inherits(ffc.AutoCompleteRenderer, goog.ui.AutoComplete.Renderer);


/**
 * Handles the user clicking on the document.
 * @param {Object} e The document click event.
 * @private
 */
ffc.AutoCompleteRenderer.prototype.handleDocumentMousedown_ = function (e) {
  this.hiliteNone();
  e.stopPropagation();
};