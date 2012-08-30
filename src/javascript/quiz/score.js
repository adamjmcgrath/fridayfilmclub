// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview A score board.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
goog.provide('ffc.quiz.Score');

goog.require('ffc.quiz.Component');
goog.require('ffc.template.quiz');

goog.require('goog.dom.classes');
goog.require('goog.string');



/**
 * Score constructor.
 * @param {number} score The user's current score.
 * @param {number} numClues The number of clues the user has been given.
 * @constructor
 */
ffc.quiz.Score = function(score, numClues) {
  goog.base(this);

  /**
   * The number of clues.
   * @type {number}
   * @private
   */
  this.numClues_ = numClues;

  /**
   * The current points available.
   * @type {number}
   * @private
   */
  this.score_ = score;

  /**
   * The elements that show the users score.
   * @type {Array.<Element>}
   * @private
   */
   this.pointEls_ = null;

  /**
   * The elements that show how many clues the user has had.
   * @type {Array.<Element>}
   * @private
   */
  this.clueBars_ = null;
};
goog.inherits(ffc.quiz.Score, ffc.quiz.Component);


/**
 * Create the clue dom.
 */
ffc.quiz.Score.prototype.createDom = function() {
  var score = goog.string.padNumber(this.score_, 2).split('');

  this.decorateInternal(soy.renderAsFragment(ffc.template.quiz.score,
      {score: score, clueCount: this.numClues_}));
};


/**
 * @override
 */
ffc.quiz.Score.prototype.decorateInternal = function(element) {
  goog.base(this, 'decorateInternal', element);

  this.pointEls_ = this.getElementsByClass('point');
  this.clueBars_ = this.getElementsByClass('bar');
};


/**
 * Update the score board.
 * @param {number} score The user's current score.
 * @param {number} numClues The number of clues the user has been given.
 */
ffc.quiz.Score.prototype.updateScore = function(score, numClues) {
  this.numClues_ = numClues;
  this.score_ = score;

  var points = goog.string.padNumber(this.score_, 2);

  this.pointEls_[0].innerHTML = points[0];
  this.pointEls_[1].innerHTML = points[1];

  for (var i = 0; i < this.numClues_; i++) {
    var clueBar = this.clueBars_[i];
    if (clueBar) {
      goog.dom.classes.add(clueBar, 'bar-active');
    }
  }
};


/**
 * @override
 */
ffc.quiz.Score.prototype.deocrateInternal = function() {
  goog.base(this, 'decorateInternal');
  this.pointEls_ = null;
  this.clueBars_ = null;
};
