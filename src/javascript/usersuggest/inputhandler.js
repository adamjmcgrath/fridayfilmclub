// Copyright Friday Film Club All Rights Reserved.

/**
 * @fileoverview Input handler that handles the enter key press.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.usersuggest.InputHandler');

goog.require('goog.ui.ac.RichInputHandler');



/**
 * InputHandler constructor.
 * @param {?string=} opt_separators Separators to split multiple entries.
 *     If none passed, uses ',' and ';'.
 * @param {?string=} opt_literals Characters used to delimit text literals.
 * @param {?boolean=} opt_multi Whether to allow multiple entries
 *     (Default: true).
 * @param {?number=} opt_throttleTime Number of milliseconds to throttle
 *     keyevents with (Default: 150). Use -1 to disable updates on typing. Note
 *     that typing the separator will update autocomplete suggestions.
 * @constructor
 */
ffc.usersuggest.InputHandler = function(opt_separators, opt_literals,
    opt_multi, opt_throttleTime) {
  goog.base(this, opt_separators, opt_literals, opt_multi, opt_throttleTime);
};
goog.inherits(ffc.usersuggest.InputHandler, goog.ui.ac.RichInputHandler);


/**
 * Handles a key event.
 * @param {goog.events.BrowserEvent} e Browser event object.
 * @return {boolean} True if the key event was handled.
 * @protected
 */
ffc.usersuggest.InputHandler.prototype.handleKeyEvent = function(e) {
  if (e.keyCode == goog.events.KeyCodes.ENTER) {
    e.preventDefault();
    this.getAutoComplete().inputEnterPressed();
  }
  return goog.base(this, 'handleKeyEvent', e);
};
