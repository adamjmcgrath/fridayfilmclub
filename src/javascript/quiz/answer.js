// Copyright 2012 Friday Film Club All Rights Reserved.

/**
 * @fileoverview An answer element.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
goog.provide('ffc.quiz.Answer');

goog.require('ffc.quiz.Component');



/**
 * Answer constructor.
 * @param {ffc.quiz.AnswerModel} model The answer model.
 * @constructor
 */
ffc.quiz.Answer = function(model) {
  goog.base(this);

  /**
   * @type {boolean}
   * @private
   */
  this.correct_ = model.correct;

  /**
   * @type {string}
   * @private
   */
  this.title_ = model.title;

  /**
   * @type {number}
   * @private
   */
  this.year_ = model.year;

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
