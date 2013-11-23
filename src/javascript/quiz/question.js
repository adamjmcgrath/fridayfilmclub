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
goog.require('ffc.quiz.QuestionModel');
goog.require('ffc.quiz.Score');
goog.require('goog.array');
goog.require('goog.fx.dom.Scroll');
goog.require('goog.net.EventType');
goog.require('goog.net.XhrIo');
goog.require('goog.ui.Component');
goog.require('goog.ui.ScrollFloater');
goog.require('goog.uri.utils');



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
   * Scroll floater for the score board.
   * @type {goog.ui.ScrollFloater}
   * @private
   */
  this.scrollfloater_ = new goog.ui.ScrollFloater();

  /**
   * @type {goog.net.XhrIo}
   * @private
   */
  this.xhr_ = new goog.net.XhrIo();

  /**
   * @type {string}
   * @private
   */
  this.url_ = goog.string.subs(ffc.quiz.Question.URI_, key);

  this.setModel(new ffc.quiz.QuestionModel());

  this.eh_.listen(this.xhr_, goog.net.EventType.COMPLETE,
      this.onResponse_, false, this);
  this.xhr_.send(this.url_);
};
goog.inherits(ffc.quiz.Question, goog.ui.Component);
goog.exportSymbol('ffc.quiz.Question', ffc.quiz.Question);


/**
 * The question API endpoint for getting question data and posting guesses.
 * @type {string}
 * @private
 */
ffc.quiz.Question.URI_ = '/api/question/%s';


/**
 * @override
 */
ffc.quiz.Question.prototype.render = function(parent) {
  var clues = this.model_.clues;

  // Create the score board and add it as a child so it get's cleaned up
  // with the question, but render it somewhere else (in the sidebar).
  this.score_ = new ffc.quiz.Score(this.model_.score, clues.length);
  this.addChild(this.score_);
  this.score_.render(this.scoreParentEl_);

  // Show the first clue on render, then any further updates to clues and
  // guesses starts with the users guess, then the clue.
  this.addClue(new ffc.quiz.Clue(this.model_.lastClues.shift()));
  // Aad the rest of the clues and guesses.
  this.addCluesAndGuesses();

  // Add the correct answer if the question is complete, or add the answer form.
  if (this.model_.answer) {
    this.addChild(new ffc.quiz.Answer(this.model_.answer), true);
  } else {
    this.answerForm = new ffc.quiz.AnswerForm();
    this.addChild(this.answerForm, true);
    this.score_.startClock();
  }

  goog.base(this, 'render', parent);
};


/**
 * @override
 */
ffc.quiz.Question.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');

  if (this.answerForm) {
    this.eh_.listen(this.answerForm, ffc.quiz.AnswerForm.MAKE_GUESS,
        this.onGuess_, false, this);
  }
  this.scrollfloater_.decorate(goog.dom.getAncestorByClass(this.scoreParentEl_, 'well'));

  // Clean up after unload.
  this.eh_.listen(window, goog.events.EventType.UNLOAD,
      this.dispose, false, this);
};


/**
 * Add clues and guesses to the question.
 */
ffc.quiz.Question.prototype.addCluesAndGuesses = function() {
  var clues = this.model_.lastClues;
  var guesses = this.model_.lastGuesses;
  // If the answer form is present, we add the child at the childCount - 1,
  // otherwise we add the child to the end.
  var addIndex = this.answerForm && this.answerForm.isInDocument() ? -1 : 0;

  // If the question has been answered,
  // don't show the last guess (as this is the answer).
  if (this.model_.answer) {
    guesses.pop();
  }

  for (i = 0, len = guesses.length; i < len; i++) {
    var index = this.getChildCount() + addIndex;
    this.addGuess(new ffc.quiz.Guess(guesses[i]), index);
    clue = clues[i];
    if (clue) {
      this.addClue(new ffc.quiz.Clue(clue), index + 1);
    }
  }
  this.scrollToBottom();
};


/**
 * Add the answer, remove the answer form.
 */
ffc.quiz.Question.prototype.addAnswer = function() {
  this.removeChild(this.answerForm, true);
  this.addChild(new ffc.quiz.Answer(this.model_.answer), true);
  this.scrollToBottom();
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
 * Update the question with an updated model.
 */
ffc.quiz.Question.prototype.update = function() {
  this.score_.updateScore(this.model_.score, this.model_.clues.length);

  if (this.model_.answer) {
    // If the question is complete add the answer.
    var callback = goog.bind(this.addAnswer, this);
    if (!this.model_.answer.correct) {
      this.answerForm.showIncorrect(callback);
    } else {
      callback();
    }
	  // Update the score and stop the clock.
    this.score_.countDown();
	  this.score_.stopClock();
  } else {
    // Otherwise add more clues and guesses.
    this.answerForm.showIncorrect(goog.bind(this.addCluesAndGuesses, this));
  }
};


/**
 * @param {ffc.quiz.AnswerFormEvent} e The event obj.
 * @private
 */
ffc.quiz.Question.prototype.onGuess_ = function(e) {
  var guess = e.guess;
  // Post the guess to the question api.
  this.xhr_.send(this.url_, 'POST',
      goog.uri.utils.buildQueryDataFromMap({'guess': guess}));
};


/**
 * @param {ffc.quiz.AnswerFormEvent} e The event obj.
 * @private
 */
ffc.quiz.Question.prototype.onResponse_ = function(e) {
  this.model_.update(e.target.getResponseJson());
  if (this.isInDocument()) {
    this.update();
  } else {
    this.render(this.parentEl_);
  }
};


/**
 * Scroll to the bottom of the page
 */
ffc.quiz.Question.prototype.scrollToBottom = function() {
    var body = document.body;
    var scrollLeft = document.body.scrollLeft;
    (new goog.fx.dom.Scroll(body, [scrollLeft, body.scrollTop],
        [body.scrollLeft, body.scrollHeight - window.innerHeight], 500)).play()
};


/**
 * @override
 */
ffc.quiz.Question.prototype.disposeInternal = function(e) {
  goog.base(this, 'disposeInternal');
  this.eh_.dispose();
  this.score_.disposeInternal();
  this.scrollfloater_.dispose();
  this.xhr_.dispose();
  this.clues_ = null;
  this.guesses_ = null;
  this.parentEl_ = null;
  this.scoreParentEl_ = null;
  this.url_ = null;
};
