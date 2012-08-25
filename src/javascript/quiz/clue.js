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
 * @param {number} position The position of the clue.
 * @param {Object} data The data to populate the clue.
 * @constructor
 */
ffc.quiz.Clue = function(position, data) {
  goog.base(this);

  /**
   * The number of the clue.
   * @type {number}
   * @private
   */
  this.position_ = position;

  /**
   * The text for the clue.
   * @type {string}
   * @private
   */
  this.text_ = data['text'];

  /**
   * The path to the image clue.
   * @type {string}
   * @private
   */
  this.image_ = data['image'];

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
