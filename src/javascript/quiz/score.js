// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview A score board.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
goog.provide('ffc.quiz.Score');

goog.require('ffc.quiz.Component');
goog.require('ffc.template.quiz');

goog.require('goog.Timer');
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
   * Event handler for this object.
   * @type {goog.events.EventHandler}
   * @private
   */
  this.eh_ = this.getHandler();

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

  /**
   * The countdown timer for animating the points display.
   * @type {goog.Timer}
   * @private
   */
  this.countDownTimer_ = new goog.Timer(ffc.quiz.Score.COUNTDOWN_INTERVAL_);
};
goog.inherits(ffc.quiz.Score, ffc.quiz.Component);


/**
 * Interval for the countdown animation..
 * @type {number}
 * @private
 */
ffc.quiz.Score.COUNTDOWN_INTERVAL_ = 200;


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

  this.eh_.listen(this.countDownTimer_, goog.Timer.TICK,
      goog.bind(this.countDown_, this, score));
  this.countDownTimer_.start();

  for (var i = 0; i < this.numClues_; i++) {
    var clueBar = this.clueBars_[i];
    if (clueBar) {
      goog.dom.classes.add(clueBar, 'bar-active');
    }
  }
};


/**
 * Animate the updating of the score board.
 * @param {number} newScore The new score to update the board with.
 * @private
 */
ffc.quiz.Score.prototype.countDown_ = function(newScore) {
  this.score_ -= 1;

  var points = goog.string.padNumber(this.score_, 2);
  this.pointEls_[0].innerHTML = points[0];
  this.pointEls_[1].innerHTML = points[1];

  if (this.score_ == newScore) {
    this.countDownTimer_.stop();
    this.eh_.unlisten(this.countDownTimer_, goog.Timer.TICK);
  }
};


/**
 * @override
 */
ffc.quiz.Score.prototype.disposeInternal = function() {
  goog.base(this, 'disposeInternal');
  this.pointEls_ = null;
  this.clueBars_ = null;
};
