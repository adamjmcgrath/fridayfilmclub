// Copyright 2012 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Handles the business logic of the question. Takes data
 *     responses from the server and holds the state of the question.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.quiz.QuestionModel');

goog.require('ffc.quiz.AnswerModel');
goog.require('ffc.quiz.ClueModel');
goog.require('ffc.quiz.GuessModel');

goog.require('goog.array');



/**
 * Question Model constructor.
 * @constructor
 */
ffc.quiz.QuestionModel = function() {
  /**
   * The answer (only available when the question is complete).
   * @type {ffc.quiz.AnswerModel}
   */
  this.answer = null;

  /**
   * An array of clues that have been given to the user.
   * @type {Array.<ffc.quiz.ClueModel>}
   */
  this.clues = [];

  /**
   * Whether the question has been completed.
   * @type {boolean}
   */
  this.complete = false;

  /**
   * Whether the question has been answered correctly.
   * @type {boolean}
   */
  this.correct = false;

  /**
   * An array of guesses the user has made.
   * @type {Array.<ffc.quiz.GuessModel>}
   */
  this.guesses = [];

  /**
   * The last clue or clues given to the user.
   * @type {Array.<ffc.quiz.ClueModel>}
   */
  this.lastClues = [];

  /**
   * The last guess or guesses from the user.
   * @type {Array.<ffc.quiz.GuessModel>}
   */
  this.lastGuesses = [];

  /**
   * The users current score.
   * @type {number}
   */
  this.score = 0;

};


/**
 * Update the model with a new response from the server.
 * @param {Object} data
 *   {Object=} answer
 *     {string} title The title of the answer.
 *     {string} year The year of the film answer.
 *   {Array.<Object>} clues
 *     {string=} image The path to the image clue.
 *     {string=} text The text for the clue.
 *   {boolean} correct Whether the question has been answered correctly.
 *   {Array.<Object>} guesses
 *     {string=} title The title of the film guess (blank if a pass).
 *     {string=} year The year of the film guess.
 *   {number} score The users current score.
 */
ffc.quiz.QuestionModel.prototype.update = function(data) {
  // Reset the last guess/clue arrays.
  this.lastClues.length = 0;
  this.lastGuesses.length = 0;

  var answer = data['answer'];
  var lenClues = this.clues.length;
  var lenGuesses = this.guesses.length;

  // Only get the new clues and guesses.
  var clues = goog.array.slice(data['clues'], lenClues);
  var guesses = goog.array.slice(data['guesses'], lenGuesses);
  var len = Math.max(clues.length, guesses.length);

  if (answer && !this.answer) {
    this.answer = new ffc.quiz.AnswerModel(answer, data['correct']);
  }

  for (var i = 0; i < len; i++) {
    var clue = clues[i];
    var guess = guesses[i];
    var pos = i + 1;
    if (clue) {
      var clueModel = new ffc.quiz.ClueModel(clue, lenClues + pos);
      this.clues.push(clueModel);
      this.lastClues.push(clueModel);
    }
    if (guess) {
      var guessModel = new ffc.quiz.GuessModel(guess, lenGuesses + pos);
      this.guesses.push(guessModel);
      this.lastGuesses.push(guessModel);
    }
  }

  this.score = data['score'];
};
