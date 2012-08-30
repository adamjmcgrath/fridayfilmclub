// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview The guess component.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.quiz.Guess');

goog.require('ffc.quiz.Component');
goog.require('ffc.template.quiz');



/**
 * Guess constructor.
 * @constructor
 * @param {ffc.quiz.GuessModel} model The model to populate the guess.
 */
ffc.quiz.Guess = function(model) {
  goog.base(this);

  /**
   * The title of the guess (a film title).
   * @type {string}
   * @private
   */
  this.title_ = model.title;

  /**
  * The year of the film guessed.
  * @type {string}
  * @private
   */
  this.year_ = model.year;
};
goog.inherits(ffc.quiz.Guess, ffc.quiz.Component);


/**
 * Create the guess DOM.
 */
ffc.quiz.Guess.prototype.createDom = function() {
  this.element_ = soy.renderAsFragment(ffc.template.quiz.guess,
      {title: this.title_, year: this.year_});
};
