// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 * 
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
 
goog.provide('ffc.Question');

goog.require('ffc.AutoComplete');
goog.require('ffc.Clue');
goog.require('ffc.Guess');
goog.require('ffc.Score');

goog.require('goog.events.EventType');
goog.require('goog.dom');
goog.require('goog.fx.dom.Scroll');
goog.require('goog.fx.easing');
goog.require('goog.ui.AutoComplete.EventType');



/**
 * Question constructor.
 * @constructor
 */
ffc.Question = function() {

  /**
   * @type {HTMLInputElement}
   */
  this.autoCompleteInput = goog.dom.getElement('ac');

  /**
   * @type {HTMLInputElement}
   */
  this.filmKeyInput = goog.dom.getElement('film');

  /**
   * @type {HTMLFormElement}
   */
  this.form = goog.dom.getElement('answer-form');

  /**
   *@type {ffc.AutoComplete}
   */
  this.autoComplete = new ffc.AutoComplete(this.autoCompleteInput);

  /**
   * The number of clues given to a user.
   * @type {Number}
   */
  this.numClues = goog.dom.getElementsByClass(
      ffc.Question.ClassName.CLUE).length;

  /**
   * The guesses associated with a question.
   * @type {Array.<ffc.Guess>}
   */
  this.guesses = [];

  // TODO(adamjmcgrath) Export property, init from page.
  this.init();
};
goog.exportSymbol('ffc.Question', ffc.Question);


/**
 * The maximum number of clues a player is allowed.
 * @type {number}
 * @private
 */
ffc.Question.MAX_CLUES_ = 4;


/**
 * 
 */
ffc.Question.ClassName = {
  CLUE: 'clue',
  GUESS: 'guess'
};


/**
 * @return {HTMLInputElement}
 */
ffc.Question.prototype.getAutoCompleteInput = function() {
  return this.autoCompleteInput;
};


/**
 *
 */
ffc.Question.prototype.init = function() {
  this.addEventListeners();

  var guesses = goog.dom.getElementsByClass(ffc.Question.ClassName.GUESS);

  for (var i = 0, len = guesses.length; i < len; i++) {
    this.guesses[i] = new ffc.Guess(this.autoCompleteInput);
    this.guesses[i].decorate(guesses[i]);
  }
};


/**
 *
 */
ffc.Question.prototype.addEventListeners = function() {
  goog.events.listen(this.autoComplete,
      goog.ui.AutoComplete.EventType.SUGGESTIONS_UPDATE,
      this.onAutoCompleteActivity, false, this);

  goog.events.listen(this.form, goog.events.EventType.SUBMIT,
      this.onFormSubmit, false, this);

  goog.events.listen(this.autoCompleteInput,
      [goog.events.EventType.FOCUS, goog.events.EventType.KEYDOWN],
      this.hideGuessErrors, false, this);
};


/**
 *
 */
ffc.Question.prototype.onAutoCompleteActivity = function(e) {
  // TODO(adamjmcgrath) Find a better way of getting the rows.
  var rows = this.autoComplete.getRenderer().rows_;
  var value = this.autoCompleteInput.value;
  var keyValue = '';
  for (var i = 0, len = rows.length; i < len; i++) {
    if (value == rows[i].data['title']) {
      keyValue = rows[i].data['key'];
      break;
    }
  }
  this.filmKeyInput.value = keyValue;
};


/**
 *
 */
ffc.Question.prototype.onFormSubmit = function(e) {
  e.preventDefault();
  if (!this.filmKeyInput.value) {
    var guess = goog.array.peek(this.guesses);
    guess.showHideError(true);
  } else {
    this.makeGuess();
  }
};


/**
 *
 */
ffc.Question.prototype.hideGuessErrors = function() {
  var guess = goog.array.peek(this.guesses);
  guess.showHideError(false);
};


/**
 *
 */
ffc.Question.prototype.buildGuess = function() {
  var guess = new ffc.Guess(this.autoCompleteInput);
  guess.render(this.form);
  // @TODO(adamjmcgrath) Use clue height and guess padding to calculate amount.
  ffc.Question.scrollDown(72);
  this.autoCompleteInput.focus();
  this.guesses.push(guess);
};


/**
 *
 */
ffc.Question.prototype.makeGuess = function() {
  var guess = goog.array.peek(this.guesses);
  guess.submit(this.filmKeyInput.value,
      goog.bind(this.onGuessResponse, this, guess));
};


/**
 *
 */
ffc.Question.prototype.onGuessResponse = function(guess, e) {
  var resp = e.target.getResponseJson();
  var correct = resp['correct'];
  var answer = resp['answer'];
  var score = resp['score'];
  var clue = resp['clue'];

  var guessText = this.autoCompleteInput.value;
  if (!correct) {
    guess.markAsGuessed(guessText);
    if (this.numClues < ffc.Question.MAX_CLUES_) {
      this.giveClue(clue);
      this.buildGuess();
    } else {
      this.onComplete(answer, false, score);
    }
  } else {
    guess.markAsGuessed(guessText, true);
    this.onComplete(answer, true, score);
  }
};


/**
 *
 */
ffc.Question.prototype.onComplete = function(answer, correct, score) {
  goog.dom.removeNode(this.autoCompleteInput);
  var score = new ffc.Score(answer, correct, score);
  score.render(this.form);
};


/**
 *
 */
ffc.Question.prototype.giveClue = function(clueText) {
  var clue = new ffc.Clue(this.numClues, clueText);
  this.numClues++;
  clue.render(this.form);
};




/**
 *
 */
ffc.Question.scrollDown = function(px) {
  var ds = goog.dom.getDocumentScroll();
  var anim = new goog.fx.dom.Scroll(goog.dom.getDocumentScrollElement(),
      [ds.x, ds.y], [ds.x, ds.y + px], 500, goog.fx.easing.easeOut);
  anim.play();
};