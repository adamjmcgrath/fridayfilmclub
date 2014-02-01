// @ use_closure_library=true
// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.invite.InputHandler');


goog.require('goog.ui.ac.RichInputHandler');



/**
 * Class for managing the interaction between an autocomplete object and a
 * text-input or textarea.
 * @param {?string=} opt_separators Separators to split multiple entries.
 * @param {?string=} opt_literals Characters used to delimit text literals.
 * @param {?boolean=} opt_multi Whether to allow multiple entries
 *     (Default: true).
 * @param {?number=} opt_throttleTime Number of milliseconds to throttle
 *     keyevents with (Default: 150).
 * @constructor
 * @extends {goog.ui.ac.RichInputHandler}
 */
ffc.invite.InputHandler = function(opt_separators, opt_literals, opt_multi,
                                   opt_throttleTime) {

  goog.base(this, opt_separators, opt_literals, opt_multi, opt_throttleTime);
};
goog.inherits(ffc.invite.InputHandler, goog.ui.ac.RichInputHandler);


/**
 * @inheritDocs
 */
ffc.invite.InputHandler.prototype.handleKeyEvent = function(e) {
  var rtn = goog.base(this, 'handleKeyEvent', e),
      isSeparatorKey = this.multi_ && e.charCode &&
          this.separators_.indexOf(String.fromCharCode(e.charCode)) != -1,
      value = this.getValue();

  if (isSeparatorKey && !value) {
    this.ac_.dismiss();
    e.preventDefault();
    e.stopPropagation();
    return true;
  }

  if (isSeparatorKey) {
    this.ac_.selectRow(new ffc.invite.GoogleRow(value, value));
  }

  return rtn;
};


/**
 * @inheritDocs
 */
ffc.invite.InputHandler.prototype.update = function(opt_force) {
  if (this.getValue() == ',') {
    this.ac_.getTarget().value = '';
  }
  goog.base(this, 'update', opt_force);
};