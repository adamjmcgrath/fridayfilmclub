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
 * @param {Object} data The data to populate the score.
 * @constructor
 */
ffc.quiz.Score = function(data) {
  goog.base(this);

  /**
   * The number of clues.
   * @type {number}
   * @private
   */
  this.numClues_ = data['clues'].length;

  /**
   * The current points available.
   * @type {number}
   * @private
   */
  this.score_ = ffc.quiz.Score.POINTS_[this.numClues_ - 1];

  if (data['complete'] && !data['correct']) {
    this.score_ = 0;
  }

};
goog.inherits(ffc.quiz.Score, ffc.quiz.Component);


/**
 * Score constructor.
 * @param {Object} data The data to populate the score.
 * @constructor
 */
ffc.quiz.Score.POINTS_ = [12, 8, 4, 2];


/**
 * Create the clue dom.
 */
ffc.quiz.Score.prototype.createDom = function() {
  var score = goog.string.padNumber(this.score_, 2).split('');

  this.decorateInternal(soy.renderAsFragment(ffc.template.quiz.score,
      {score: score, clueCount: this.numClues_}));
};


/**
 * 
 */
ffc.quiz.Score.prototype.decorateInternal = function(element) {
  goog.base(this, 'decorateInternal', element);

  this.pointEls_ = this.getElementsByClass('point');
  this.clueBars_ = this.getElementsByClass('bar');
};


/**
 * 
 */
ffc.quiz.Score.prototype.updateScore = function(data) {
  this.numClues_ = data['clues'].length;

  this.score_ = ffc.quiz.Score.POINTS_[this.numClues_ - 1];
  
  if (data['complete'] && !data['correct']) {
    this.score_ = 0;
  }

  var points = goog.string.padNumber(this.score_, 2);

  this.pointEls_[0].innerHTML = points[0];
  this.pointEls_[1].innerHTML = points[1];

  for (var i = 0; i < this.numClues_; i++) {
    var clueBar = this.clueBars_[i];
    if (clueBar) {
      goog.dom.classes.add(clueBar, 'bar-active');
    }
  };
};