// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 *
 * <div class="clue">
 *   <p><b>Clue #:</b> Clue text.</p>
 * </div>
 */
goog.provide('ffc.Clue');

goog.require('goog.events.EventTarget');
goog.require('goog.net.XhrIo');
goog.require('goog.string.path');



/**
 * Clue constructor.
 * @constructor
 */
ffc.Clue = function(number) {

  /**
   * The zero indexed number of the guess.
   * @type {string}
   */
  this.number = number;

  /**
   * The display number (A string representation of the number + 1).
   * @type {string}
   */
  this.displayNumber = (number + 1) + '';

  /**
   * The Clue container element.
   * @type {Element}
   */
  this.element = this.getElement();


}
goog.inherits(ffc.Clue, goog.events.EventTarget);


/**
 * Clue constructor.
 * @constructor
 */
ffc.Clue.prototype.getElement = function() {
  var id = goog.string.subs(ffc.Clue.ID_PFX_, this.displayNumber);
  return goog.dom.getElement(id);
};
