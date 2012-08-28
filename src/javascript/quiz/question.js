// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.quiz.Question');

goog.require('ffc.quiz.Answer');
goog.require('ffc.quiz.AnswerForm');
goog.require('ffc.quiz.Clue');
goog.require('ffc.quiz.Guess');
goog.require('ffc.quiz.Score');

goog.require('goog.array');
goog.require('goog.net.XhrIo');
goog.require('goog.ui.Component');
goog.require('goog.ui.ScrollFloater');



/**
 * Question constructor.
 * @param {String} key The key id of the question in the datastore.
 * @param {Element} parent The element in which to render the component once
 *     it gets a data response form the server.
 * @param {Element} scoreParent The element in which to render the score board.
 * @constructor
 */
ffc.quiz.Question = function(key, parent, scoreParent) {
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

  /**
   * The parent element to render the question.
   * @type {Element}
   * @private
   */
  this.parentEl_ = parent;

  /**
   * The score board.
   * @type {ffc.quiz.Score}
   * @private
   */
  this.score_ = null;

  /**
   * The parent element to render the score.
   * @type {Element}
   * @private
   */
  this.scoreParentEl_ = scoreParent;

  /**
   * SCroll floater for the score board.
   * @type {goog.ui.ScrollFloater}
   * @private
   */
  this.scrollfloater_ = new goog.ui.ScrollFloater();

  goog.net.XhrIo.send('/api/question/' + key, goog.bind(this.render, this));
};
goog.inherits(ffc.quiz.Question, goog.ui.Component);
goog.exportSymbol('ffc.quiz.Question', ffc.quiz.Question);


/**
 * @override
 * @param {goog.events.Event} e The xhr response event.
 */
ffc.quiz.Question.prototype.render = function(e) {
  var data = e.target.getResponseJson();
  var guess;
  var i;
  var len;

  for (i = 0, len = data['clues'].length; i < len; i++) {
    this.addClue(new ffc.quiz.Clue(i + 1, data['clues'][i]));
    guess = data['guesses'][i];
    if (guess) {
      this.addGuess(new ffc.quiz.Guess(guess));
    }
  }

  if (data['complete']) {
    this.addChild(new ffc.quiz.Answer(data), true);
  } else {
    this.answerForm = new ffc.quiz.AnswerForm();
    this.addChild(this.answerForm, true);
  }

  this.score_ = new ffc.quiz.Score(data);
  this.score_.render(this.scoreParentEl_);

  goog.base(this, 'render', this.parentEl_);
};


/**
 * @override
 */
ffc.quiz.Question.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');

  if (this.answerForm) {
    this.eh_.listen(this.answerForm, ffc.quiz.AnswerForm.ANSWER_RESPONSE,
        this.onAnswerResponse_, false, this);
  }
  
  this.scrollfloater_.decorate(this.scoreParentEl_);
};


/**
 * Add clues and guesses to the question.
 * @param {Array.Object} clues An array of clue data.
 * @param {Array.Object} guesses An array of guess data.
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
 * @param {Object} data The data.
 */
ffc.quiz.Question.prototype.addAnswer = function(data) {
  this.removeChild(this.answerForm, true);
  this.addChild(new ffc.quiz.Answer(data), true);
};


/**
 * @param {ffc.quiz.Clue} clue The clue object to add.
 * @param {number=} opt_index The index to add the clue.
 */
ffc.quiz.Question.prototype.addClue = function(clue, opt_index) {
  var index = opt_index || this.getChildCount();

  this.clues_.push(clue);
  this.addChildAt(clue, index, true);
};


/**
 * @param {ffc.quiz.Guess} guess The guess object to add.
 * @param {number=} opt_index The index to add the guess.
 */
ffc.quiz.Question.prototype.addGuess = function(guess, opt_index) {
  var index = opt_index || this.getChildCount();

  this.guesses_.push(guess);
  this.addChildAt(guess, index, true);
};


/**
 * @param {ffc.quiz.AnswerFormEvent} e The event obj.
 * @private
 */
ffc.quiz.Question.prototype.onAnswerResponse_ = function(e) {
  var callback;
  var data = e.data;

  this.score_.updateScore(data);

  if (data['complete']) {
    callback = goog.bind(this.addAnswer, this, data);
  } else {
    var clues = goog.array.slice(data['clues'], this.clues_.length);
    var guesses = goog.array.slice(data['guesses'], this.guesses_.length);
    callback = goog.bind(this.addCluesAndGuesses, this, clues, guesses);
  }
  
  if (!data['correct']) {
    this.answerForm.showIncorrect(callback);
  } else {
    callback();
  }
};
