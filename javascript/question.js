// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 */
goog.provide('ffc.Question');

goog.require('ffc.Clue');
goog.require('goog.events.EventTarget');



/**
 * Question constructor.
 * @constructor
 */
ffc.Question = function(el) {

  /**
   * The clues associated with a question.
   * @type {Array.<ffc.Clue>}
   */
  this.clues = [new ffc.FirstClue()];
 
  goog.base(this);
};
goog.inherits(ffc.Question, goog.events.eventTarget);


/**
 * The number of guesses a player is allowed.
 * @type {number}
 * @private
 */
ffc.Guess.NUM_GUESSES_ = 3;
