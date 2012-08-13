// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview The guess component.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.quiz.Guess');

goog.require('ffc.template.quiz');


/**
 * Guess constructor.
 * @constructor
 * @param {Object} data The data to populate the guess.
 */
ffc.quiz.Guess = function(data) {

  /**
   * The title of the guess (a film title).
   * @type {string}
   * @private
   */
  this.title_ = data.title;

  /**
  * The year of the film guessed.
  * @type {string}
  * @private
   */
  this.year_ = data.year;
};
goog.inherits(ffc.quiz.Guess, goog.ui.Component);


/**
 * Create the guess DOM.
 */
ffc.quiz.Guess.prototype.createDom = function() {
  this.element_ = soy.renderAsFragment(
      ffc.template.quiz.guess, {title: this.title_, year: this.year_});
};
