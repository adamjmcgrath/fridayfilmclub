// Copyright 2012 Friday Film Club All Rights Reserved.

/**
 * @fileoverview The answer model.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.quiz.AnswerModel');



/**
 * Answer Model constructor.
 * @param {Object} data
 *   {string} title The title of the answer.
 *   {string} year The year of the film answer.
 * @param {boolean} correct Whether the answer is correct.
 * @param {number} numGuesses The number of guesses required.
 * @constructor
 */
ffc.quiz.AnswerModel = function(data, correct, numGuesses) {
  /**
   * @type {string}
   */
  this.title = data['title'];

  /**
   * @type {number}
   */
  this.year = data['year'];

  /**
   * @type {boolean}
   */
  this.correct = correct;

  /**
   * @type {number}
   */
  this.numGuesses = numGuesses;
};
