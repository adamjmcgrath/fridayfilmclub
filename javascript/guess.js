// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 */
goog.provide('ffc.Guess');

goog.require('goog.events.EventTarget');

goog.require('ffc.AutoComplete');
goog.require('ffc.ClarifyDialog');
goog.require('ffc.Clue');



/**
 * Guess constructor.
 * @constructor
 * @param {number} number The number of the guess (zero indexed).
 */
ffc.Guess = function(number) {

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

}
goog.inherits(ffc.Guess, goog.events.eventTarget);
