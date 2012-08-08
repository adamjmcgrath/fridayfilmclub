// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview A clue element.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
goog.provide('ffc.Clue');

goog.require('goog.fx.dom.FadeInAndShow');
goog.require('goog.ui.Component');



/**
 * Clue constructor.
 * @constructor
 */
ffc.Clue = function(position, data) {
  goog.base(this);

  /**
   * The number of the clue.
   * @type {number}
   */
  this.position_ = position;

  /**
   * The text for the clue.
   * @type {string}
   */
  this.text_ = data.text;

  /**
   * The path to the image clue.
   * @type {string}
   */
  this.image_ = data.image;

};
goog.inherits(ffc.Clue, goog.ui.Component);


/**
 *
 */
ffc.Clue.prototype.createDom = function() {
  this.element_ = soy.renderAsFragment(
      ffc.template.quiz.clue,
      {position: this.position_, text: this.text_, image: this.image_});
};


/**
 *
 */
ffc.Clue.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');

  (new goog.fx.dom.FadeInAndShow(this.element_, 500)).play();
};
