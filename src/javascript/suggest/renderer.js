// @ use_closure_library=true
// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.suggest.AutoCompleteRenderer');

goog.require('goog.ui.ac.Renderer');



/**
 * AutoComplete constructor.
 * @param {Element} parent The parent in which to render the auto complete.
 * @param {{renderRow: function() {}}}
 * @constructor
 */
ffc.suggest.AutoCompleteRenderer = function(parent, customRenderer) {
  goog.base(this, parent, customRenderer);
};
goog.inherits(ffc.suggest.AutoCompleteRenderer, goog.ui.ac.Renderer);


/**
 * Handles the user clicking on the document.
 * @param {Object} e The document click event.
 * @private
 */
ffc.suggest.AutoCompleteRenderer.prototype.handleDocumentMousedown_ =
    function(e) {
  this.hiliteNone();
  e.stopPropagation();
};
