// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview A score element.
 *
 * <div id="answer">
 *   <p>
 *     <b>
 *       (C|Inc)orrect. You scored (x).
 *     </b>
 *     The answer is of course: <b>(Answer).</b>
 *   </p>
 * </div> 
 * 
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.Score');

goog.require('ffc.Guess');

goog.require('goog.dom');
goog.require('goog.string');



/**
 * Score constructor.
 * @constructor
 */
ffc.Score = function(answer, correct, score) {

  /**
   * @type {string}
   */
  this.answer = answer;

  /**
   * @type {boolean}
   */
  this.correct = correct;

  /**
   * @type {number}
   */
  this.score = score;

};


/**
 * @type {string}
 */
ffc.Score.TPL = '<p><b>%s. You scored %s.</b>' +
                 'The answer is of course: <b>%s.</b></p>';


/**
 * @type {string}
 */
ffc.Score.CONTAINER = 'answer';


/**
 *
 */
ffc.Score.prototype.render = function(parent) {
  var container = goog.dom.createDom(goog.dom.TagName.DIV,
      {'id': ffc.Score.CONTAINER});

  var msg = this.correct ?
      ffc.Guess.Message.CORRECT : ffc.Guess.Message.INCORRECT;

  container.innerHTML = goog.string.subs(
      ffc.Score.TPL, msg, this.score, this.answer);

  parent.appendChild(container);
};
