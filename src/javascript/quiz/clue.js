// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview A clue element.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
goog.provide('ffc.quiz.Clue');

goog.require('ffc.quiz.Component');
goog.require('ffc.template.quiz');



/**
 * Clue constructor.
 * @param {ffc.quiz.ClueModel} model The clue model.
 * @constructor
 */
ffc.quiz.Clue = function(model) {
  goog.base(this);

  /**
   * The number of the clue.
   * @type {number}
   * @private
   */
  this.position_ = model.position;

  /**
   * The text for the clue.
   * @type {string}
   * @private
   */
  this.text_ = model.text;

  /**
   * The path to the image clue.
   * @type {string}
   * @private
   */
  this.image_ = model.image;

};
goog.inherits(ffc.quiz.Clue, ffc.quiz.Component);


/**
 * Create the clue dom.
 */
ffc.quiz.Clue.prototype.createDom = function() {
  this.element_ = soy.renderAsFragment(
      ffc.template.quiz.clue,
      {position: this.position_, text: this.text_, image: this.image_});
};
