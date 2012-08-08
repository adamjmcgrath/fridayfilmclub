// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.Guess');

goog.require('ffc.template.quiz');


/**
 * Guess constructor.
 * @constructor
 * @param {string} text The users incorrect guess..
 */
ffc.Guess = function(data) {

  /**
   *
   */
  this.title_ = data.title;

  /**
   *
   */
  this.year_ = data.year;
};
goog.inherits(ffc.Guess, goog.ui.Component);


/**
 *
 */
ffc.Guess.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');

  (new goog.fx.dom.FadeInAndShow(this.element_, 500)).play();
};



/**
 *
 */
ffc.Guess.prototype.createDom = function() {
  this.element_ = soy.renderAsFragment(
      ffc.template.quiz.guess, {title: this.title_, year: this.year_});
};
