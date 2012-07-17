// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 *
 * <form class="well" id="answer-form">
 *   <div class="input-prepend form-horizontal guess">
 *     <span class="add-on"><i class="icon-search"></i></span>
 *     <input type="text" autocomplete="off" id="ac" class="span7" aria-haspopup="true">
 *     <input id="film" type="hidden" name="guess" value="">
 *     <button type="submit" class="btn">Search</button>
 *   </div>
 *   <div class="controls rows" id="suggestions">
 *     <p>Search for a film, then select your guess from the list.</p>
 *     <!-- <label class="radio">
 *       <input type="radio" name="guess" value="">
 *       Once Upon a Time in the West<span>1982</span>
 *     </label> -->
 *     <div class="guess-buttons">
 *       <a href="#" class="btn btn-primary">Submit</a>
 *       <a href="#" class="btn btn-danger">Pass</a>
 *     </div>
 *   </div>
 * </form>
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
  DISABLED: 'disabled',
  ERROR: 'error',
  INCORRECT: 'incorrect',
  INPUT: ['input', 'grid-5'],
  BUTTON: ['button', 'grid-2', 'disabled']
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


/**
 * 
 */
ffc.Guess.prototype.showHideError = function(error) {
  goog.dom.classes.enable(this.buttonWrap, ffc.Guess.ClassName.DISABLED, error);
  goog.dom.classes.enable(this.inputWrap, ffc.Guess.ClassName.ERROR, error);
};
