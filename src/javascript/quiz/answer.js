// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview An answer element.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
goog.provide('ffc.Answer');

goog.require('goog.fx.dom.FadeInAndShow');
goog.require('goog.ui.Component');



/**
 * Answer constructor.
 * @constructor
 */
ffc.Answer = function(data) {
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
goog.inherits(ffc.Answer, goog.ui.Component);


/**
 *
 */
ffc.Answer.prototype.createDom = function() {
  this.element_ = soy.renderAsFragment(
      ffc.template.quiz.answer,
      {correct: this.correct_, title: this.title_, year: this.year_});
};


/**
 *
 */
ffc.Answer.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');

  (new goog.fx.dom.FadeInAndShow(this.element_, 500)).play();
};
