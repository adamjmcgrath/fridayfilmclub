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
ffc.quiz.Score.COUNTDOWN_INTERVAL_ = 1000;


/**
 * Create the clue dom.
 */
ffc.quiz.Score.prototype.createDom = function() {
  var score = goog.string.padNumber(this.score_, 5).split('');

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
 * @override
 */
ffc.quiz.Score.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');

  this.eh_.listen(this.countDownTimer_, goog.Timer.TICK,
      this.countDown, false, this);
};


/**
 * Update the score board.
 * @param {number} score The user's current score.
 * @param {number} numClues The number of clues the user has been given.
 */
ffc.quiz.Score.prototype.updateScore = function(score, numClues) {
  this.score_ = score;
  this.numClues_ = numClues;

  for (var i = 0; i < (this.numClues_ - 1); i++) {
    var clueBar = this.clueBars_[i];
    if (clueBar) {
      goog.dom.classes.add(clueBar, 'bar-active');
    }
  }
};


/**
 * Start ticking the score down.
 */
ffc.quiz.Score.prototype.startClock = function() {
  this.countDownTimer_.start();
};


/**
 * Start ticking the score down.
 */
ffc.quiz.Score.prototype.stopClock = function() {
  this.countDownTimer_.stop();
};


/**
 * Animate the updating of the score board.
 */
ffc.quiz.Score.prototype.countDown = function() {
  if (!this.score_) {
    this.stopClock();
  } else {
    this.score_ -= 1;
  }

  var points = goog.string.padNumber(this.score_, 5);
  goog.array.forEach(this.pointEls_, function(el, i) {
    el.innerHTML = points[i];
  });
};


/**
 * @override
 */
ffc.quiz.Score.prototype.disposeInternal = function() {
  goog.base(this, 'disposeInternal');
  this.pointEls_ = null;
  this.clueBars_ = null;
};
