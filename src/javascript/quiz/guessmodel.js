// Copyright 2012 Friday Film Club All Rights Reserved.

/**
 * @fileoverview A guess is an answer that hasn't been verified as correct or
 *     not, also can be a 'pass'.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.quiz.GuessModel');



/**
 * Guess Model constructor.
 * @param {Object} data
 *   {string} title The title of the answer.
 *   {string} year The year of the film answer.
 * @param {number} position The number of the guess.
 * @constructor
 */
ffc.quiz.GuessModel = function(data, position) {
  /**
   * @type {string}
   */
  this.title = data['title'];

  /**
   * @type {number}
   */
  this.year = data['year'];

  /**
   * The position of the clue.
   * @type {number}
   */
  this.position = position;
};

