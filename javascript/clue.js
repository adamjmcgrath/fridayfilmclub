// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
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

  /**
   * The XhrIo instance for retrieving the clue fomr the server.
   * @type {Element}
   */
  this.xhrIo = new goog.net.XhrIo();

}
goog.inherits(ffc.Clue, goog.events.eventTarget);


/**
 * Prefix for clue element's id.
 * @type {string}
 */
ffc.Clue.ID_PFX_ = 'clue-%s';


/**
 * The base path for fetching clues.
 * @type {string}
 */
ffc.Clue.ROOT_PATH_ = '/rpc/get_clue';


/**
 * Add event listeners to the clue.
 */
ffc.Clue.prototype.addEventListeners = function() {
  

};


/**
 * Clue constructor.
 * @constructor
 */
ffc.Clue.prototype.getElement = function() {
  var id = goog.string.subs(ffc.Clue.ID_PFX_, this.displayNumber);
  return goog.dom.getElement(id);
};


/**
 * Clue constructor.
 * @constructor
 */
ffc.Clue.prototype.getClue = function() {
  var path = goog.string.path.join(ffc.Clue.ROOT_PATH_, this.number);
  this.xhrIo = new goog.net.XhrIo();
};

