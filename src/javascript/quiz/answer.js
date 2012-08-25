// Copyright 2012 Friday Film Club All Rights Reserved.

/**
 * @fileoverview An answer element.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
goog.provide('ffc.quiz.Answer');

goog.require('ffc.quiz.Component');



/**
 * Answer constructor.
 * @param {Object} data The answer data obj.
 * @constructor
 */
ffc.quiz.Answer = function(data) {
  goog.base(this);

  /**
   * @type {boolean}
   * @private
   */
  this.correct_ = data['correct'];

  /**
   * @type {string}
   * @private
   */
  this.title_ = data['answer']['title'];

  /**
   * @type {string}
   * @private
   */
  this.year_ = data['answer']['year'];

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
