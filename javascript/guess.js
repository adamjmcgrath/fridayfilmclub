// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 *
 * <div class="guess grids (incorrect)">
 *   <div class="input grid-5">
 *     (<p><span>Incorrect Guess</span></p>)
 *     (<input type="text" autocomplete="off" id="ac">)
 *   </div>
 *   <div class="button grid-2">
 *     <p>
 *       <button (disabled="disabled")>
 *         <span>(Incorrect|Correct|Submit)</span>
 *       </button>
 *     </p>
 *   </div>
 * </div>
 */
goog.provide('ffc.Guess');

goog.require('goog.dom');
goog.require('goog.dom.TagName');
goog.require('goog.events');
goog.require('goog.events.EventTarget');

goog.require('ffc.AutoComplete');
goog.require('ffc.ClarifyDialog');
goog.require('ffc.Clue');



/**
 * Guess constructor.
 * @constructor
 * @param {number} number The number of the guess (zero indexed).
 */
ffc.Guess = function(question) {
  /**
   *
   */
  this.question = question;

  /**
   * The XhrIo instance for retrieving the clue from the server.
   * @type {Element}
   */
  this.xhrIo = new goog.net.XhrIo();

  goog.base(this);
}
goog.inherits(ffc.Guess, goog.events.EventTarget);


/**
 * 
 */
ffc.Guess.ClassName = {
  ROOT: ['guess', 'grids'],
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
ffc.Guess.prototype.render = function() {
  this.inputWrap = goog.dom.createDom(goog.dom.TagName.DIV,
      ffc.Guess.ClassName.INPUT, this.question.getAutoComplete().getTarget());

  this.buttonMessage = goog.dom.createDom(goog.dom.TagName.SPAN,
     null, ffc.Guess.Message.SUBMIT);

  this.button = goog.dom.createDom(goog.dom.TagName.BUTTON,
        null, this.buttonMessage);

  var buttonWrapInner = goog.dom.createDom(goog.dom.TagName.DIV,
     ffc.Guess.ClassName.BUTTON);
  this.buttonWrap = goog.dom.createDom(goog.dom.TagName.DIV,
     ffc.Guess.ClassName.BUTTON, buttonWrapInner);

  this.root = goog.dom.createDom(goog.dom.TagName.DIV,
      ffc.Guess.ClassName.ROOT, this.input, this.buttonWrap);
};


/**
 * 
 */
ffc.Guess.prototype.addEventListeners = function() {
  goog.events.addEventListener(this.button, goog.events.EventType.CLICK,
      this.submit, false, this);
};


/**
 * 
 */
ffc.Guess.prototype.getDom = function() {
  return this.root;
};


/**
 * 
 */
ffc.Guess.prototype.getInputWrap = function() {
  return this.inputWrap;
};


/**
 * 
 */
ffc.Guess.prototype.submit = function() {
  goog.net.XhrIo.send(ffc.Guess.URI, goog.bind(this.handleResponse), 'POST',
      'guess=' + this.question.getAutoComplete().getKeyInput().value);
};


/**
 * 
 */
ffc.Guess.prototype.handleResponse = function(e) {
  console.log(e.target.getResponseJson);
};
