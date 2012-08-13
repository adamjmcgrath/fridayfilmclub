// Copyright 2012 Friday Film Club All Rights Reserved.

/**
 * @fileoverview An answer element.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
goog.provide('ffc.quiz.Answer');

goog.require('ffc.quiz.Component');



/**
 * Answer constructor.
 * @constructor
 */
ffc.quiz.Answer = function(data) {
  goog.base(this);

  /**
   * @type {boolean}
   */
  this.correct_ = data.correct;

  /**
   * @type {string}
   */
  this.title_ = data.answer.title;

  /**
   * @type {string}
   */
  this.year_ = data.answer.year;

};
goog.inherits(ffc.quiz.Answer, ffc.quiz.Component);


/**
 * Create the answer's DOM.
 */
ffc.quiz.Answer.prototype.createDom = function() {
  this.element_ = soy.renderAsFragment(
      ffc.template.quiz.answer,
      {correct: this.correct_, title: this.title_, year: this.year_});
};
