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
  this.model_ = model;
};
goog.inherits(ffc.quiz.Answer, ffc.quiz.Component);


/**
 * Create the answer's DOM.
 */
ffc.quiz.Answer.prototype.createDom = function() {
  this.element_ = soy.renderAsFragment(
      ffc.template.quiz.answer, {
        correct: this.model_.correct,
        title: this.model_.title,
        year: this.model_.year,
        score: this.model_.score,
        numGuesses: this.model_.numGuesses
      });
};
