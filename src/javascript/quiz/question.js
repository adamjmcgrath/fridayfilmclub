// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 * 
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
 
goog.provide('ffc.quiz.Question');

goog.require('goog.array');
goog.require('goog.net.XhrIo');
goog.require('goog.ui.Component');

goog.require('ffc.quiz.Answer');
goog.require('ffc.quiz.AnswerForm');
goog.require('ffc.quiz.Clue');
goog.require('ffc.quiz.Guess');



/**
 * Question constructor.
 * @param {String} key The key id of the question in the datastore.
 * @constructor
 */
ffc.quiz.Question = function(key, element) {
  goog.base(this);
  
  /**
   * The key id of the question in the datastore.
   * @private
   * @type {String}
   */
  this.key_ = key;

  /**
   * Event handler for this object.
   * @type {goog.events.EventHandler}
   * @private
   */
  this.eh_ = this.getHandler();

  /**
   * Array of clues.
   * @type {Array.<ffc.quiz.Clue>}
   * @private
   */
  this.clues_ = [];

  /**
   * Array of clues.
   * @type {Array.<ffc.quiz.Guess>}
   * @private
   */
  this.guesses_ = [];

  this.parentEl_ = element;

  goog.net.XhrIo.send('/api/question/' + key, goog.bind(this.render, this));
};
goog.inherits(ffc.quiz.Question, goog.ui.Component);
goog.exportSymbol('ffc.quiz.Question', ffc.quiz.Question);


/**
 *
 */
ffc.quiz.Question.prototype.render = function(e) {
  var data = e.target.getResponseJson(),
      i,
      guess,
      len;
  
  for (i = 0, len = data.clues.length; i < len; i++) {
    this.addClue(new ffc.quiz.Clue(i + 1, data.clues[i]));
    guess = data.guesses[i];
    if (guess) {
      this.addGuess(new ffc.quiz.Guess(guess));
    }
  }

  if (data.complete) {
    this.addChild(new ffc.quiz.Answer(data), true);
  } else {
    this.answerForm = new ffc.quiz.AnswerForm();
    this.addChild(this.answerForm, true);
  }

  goog.base(this, 'render', this.parentEl_);
};


/**
 *
 */
ffc.quiz.Question.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');

  if (this.answerForm) {
    this.eh_.listen(this.answerForm, ffc.quiz.AnswerForm.ANSWER_RESPONSE,
        this.onAnswerResponse_, false, this);
  }
};


/**
 *
 */
ffc.quiz.Question.prototype.addCluesAndGuesses = function(clues, guesses) {
  var clue;
  var clueCount = this.clues_.length;

  for (i = 0, len = guesses.length; i < len; i++) {
    this.addGuess(new ffc.quiz.Guess(guesses[i]), this.getChildCount() - 1);
    clue = clues[i];
    if (clue) {
      this.addClue(new ffc.quiz.Clue(i + 1 + clueCount, clue),
          this.getChildCount() - 1);
    }
  }
};


/**
 *
 */
ffc.quiz.Question.prototype.addClue = function(clue, opt_index) {
  var index = opt_index || this.getChildCount();
  
  this.clues_.push(clue);
  this.addChildAt(clue, index, true);
};


/**
 *
 */
ffc.quiz.Question.prototype.addGuess = function(guess, opt_index) {
  var index = opt_index || this.getChildCount();

  this.guesses_.push(guess);
  this.addChildAt(guess, index, true);
};


/**
 * @param {ffc.quiz.AnswerFormEvent} e
 */
ffc.quiz.Question.prototype.onAnswerResponse_ = function(e) {
  var data = e.data;

  if (data.complete) {
    this.removeChild(this.answerForm, true);
    this.addChild(new ffc.quiz.Answer(data), true);
  } else {
    this.answerForm.clearForm();
    var clues = goog.array.slice(data.clues, this.clues_.length);
    var guesses = goog.array.slice(data.guesses, this.guesses_.length);

    this.addCluesAndGuesses(clues, guesses);
  }
};
