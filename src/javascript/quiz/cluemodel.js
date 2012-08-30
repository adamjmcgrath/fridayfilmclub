// Copyright 2012 Friday Film Club All Rights Reserved.

/**
 * @fileoverview The clue model.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.quiz.ClueModel');



/**
 * Clue Model constructor.
 * @param {Object=} data
 *   {string=} image The path to the image clue.
 *   {string=} text The text for the clue.
 * @param {number} position The position of the clue.
 * @constructor
 */
ffc.quiz.ClueModel = function(data, position) {
  /**
   * The path to the clue image.
   * @type {string=}
   */
  this.image = data['image'];

  /**
   * The clue text.
   * @type {string}
   */
  this.text = data['text'];

  /**
   * The position of the clue.
   * @type {number}
   */
  this.position = position;
};
