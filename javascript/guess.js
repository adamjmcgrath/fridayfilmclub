// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 *
 * <div class="guess grids (incorrect)">
 *   <div class="input grid-5">
 *     <p>(<span>Incorrect Guess</span>)</p>
 *   </div>
 *   <div class="button grid-2">
 *     <p>
 *       <button (disabled="disabled")>
 *         <span>(Incorrect|Correct|Submit)</span>
 *       </button>
 *     </p>
 *   </div>
 * </div>
 * 
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.Guess');

goog.require('goog.dom');
goog.require('goog.dom.TagName');
goog.require('goog.dom.classes');
goog.require('goog.events');
goog.require('goog.net.XhrIo');
goog.require('goog.string');

goog.require('ffc.AutoComplete');
goog.require('ffc.ClarifyDialog');
goog.require('ffc.Clue');



/**
 * Guess constructor.
 * @constructor
 * @param {number} number The number of the guess (zero indexed).
 */
ffc.Guess = function(input) {

  /**
   *
   */
  this.input = input;
}


/**
 * 
 */
ffc.Guess.ClassName = {
  ROOT: ['guess', 'grids'],
  CORRECT: 'correct',
  INCORRECT: 'incorrect',
  INPUT: ['input', 'grid-5'],
  BUTTON: ['button', 'grid-2']
};


/**
 * 
 */
ffc.Guess.Message = {
  CORRECT: 'Correct',
  INCORRECT: 'Incorrect',
  SUBMIT: 'Submit'
};


/**
 * 
 */
ffc.Guess.URI = '?js=1';


/**
 * 
 */
ffc.Guess.POST = 'guess=%s';


/**
 * 
 */
ffc.Guess.prototype.render = function(parent) {
  this.input.value = '';

  var inputWrapInner = goog.dom.createDom(goog.dom.TagName.P,
      null, this.input);

  this.inputWrap = goog.dom.createDom(goog.dom.TagName.DIV,
      ffc.Guess.ClassName.INPUT, inputWrapInner);

  this.buttonMessage = goog.dom.createDom(goog.dom.TagName.SPAN,
      null, ffc.Guess.Message.SUBMIT);

  this.button = goog.dom.createDom(goog.dom.TagName.BUTTON,
      null, this.buttonMessage);

  var buttonWrapInner = goog.dom.createDom(goog.dom.TagName.P,
      null, this.button);
  this.buttonWrap = goog.dom.createDom(goog.dom.TagName.DIV,
      ffc.Guess.ClassName.BUTTON, buttonWrapInner);

  this.root = goog.dom.createDom(goog.dom.TagName.DIV,
      ffc.Guess.ClassName.ROOT, this.inputWrap, this.buttonWrap);

  parent.appendChild(this.root);
};


/**
 * 
 */
ffc.Guess.prototype.decorate = function(parent) {

  this.root = goog.dom.getElement(parent);

  this.inputWrap = goog.dom.getElementByClass(
      ffc.Guess.ClassName.INPUT, this.root);

  this.buttonWrap = goog.dom.getElementByClass(
      ffc.Guess.ClassName.BUTTON, this.root);

  this.button = this.buttonWrap.getElementsByTagName(
      goog.dom.TagName.BUTTON)[0];

  this.buttonMessage = this.button.getElementsByTagName(
      goog.dom.TagName.SPAN)[0];

};


/**
 * 
 */
ffc.Guess.prototype.submit = function(value, callback) {
  goog.net.XhrIo.send(ffc.Guess.URI, callback, 'POST',
      goog.string.subs(ffc.Guess.POST, value));
};


/**
 * 
 */
ffc.Guess.prototype.markAsGuessed = function(guessText, correct) {
  this.button.disabled = 'disabled';
  goog.dom.classes.enable(this.root, ffc.Guess.ClassName.CORRECT, correct);
  goog.dom.classes.enable(this.root, ffc.Guess.ClassName.INCORRECT, !correct);
  var msg = correct ? ffc.Guess.Message.CORRECT : ffc.Guess.Message.INCORRECT;
  this.buttonMessage.innerHTML = msg;

  var guessTextWrap = goog.dom.createDom(goog.dom.TagName.SPAN, null,
      guessText);
  // @TODO(amcgrath) Clean up this reference.
  var wrap = this.inputWrap.getElementsByTagName(goog.dom.TagName.P)[0];
  wrap.appendChild(guessTextWrap);
};
