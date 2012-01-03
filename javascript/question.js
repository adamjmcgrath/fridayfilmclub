// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 */
goog.provide('ffc.Question');

goog.require('ffc.AutoComplete');
goog.require('ffc.Clue');
goog.require('goog.events.EventTarget');



/**
 * Question constructor.
 * @constructor
 */
ffc.Question = function() {

  /**
   *
   */
  this.autoComplete = new ffc.AutoComplete(document.getElementById('ac'),
      'film');

  /**
   * The clues associated with a question.
   * @type {Array.<ffc.Clue>}
   */
  this.clues = [];

  goog.base(this);
};
goog.inherits(ffc.Question, goog.events.EventTarget);
goog.exportSymbol('ffc.Question', ffc.Question);


/**
 * 
 */
ffc.Question.prototype.getAutoComplete = function() {
  return this.autoComplete;
};


/**
 * The number of guesses a player is allowed.
 * @type {number}
 * @private
 */
ffc.Question.NUM_GUESSES_ = 3;
