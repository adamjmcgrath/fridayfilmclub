// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview The Answer form.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.quiz.AnswerForm');
goog.provide('ffc.quiz.AnswerFormEvent');

goog.require('ffc.quiz.Component');
goog.require('ffc.suggest.AutoComplete');
goog.require('ffc.template.quiz');

goog.require('goog.dom.forms');
goog.require('goog.events.Event');
goog.require('goog.events.EventType');
goog.require('goog.net.XhrIo');

goog.require('soy');



/**
 * Answer form constructor.
 * @constructor
 */
ffc.quiz.AnswerForm = function() {
  goog.base(this);

  this.eh_ = this.getHandler();
};
goog.inherits(ffc.quiz.AnswerForm, ffc.quiz.Component);


/**
 * @type {string} Uri to submit the answer to.
 * @private
 */
ffc.quiz.AnswerForm.URI_ = '';


/**
 * @override
 */
ffc.quiz.AnswerForm.prototype.createDom = function() {
  this.decorateInternal(soy.renderAsFragment(ffc.template.quiz.answerForm));
};


/**
 * @override
 */
ffc.quiz.AnswerForm.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');

  this.suggestInfo_ = this.getElementByClass('suggest-info');

  this.acInput_ = this.getElementByClass('autocomplete');
  this.ac_ = new ffc.suggest.AutoComplete(this.acInput_,
      this.getElementByClass('suggestions'));

  this.eh_.listen(this.dom_.getElement('btn-clear'),
      goog.events.EventType.CLICK, this.onClear_);

  this.eh_.listen(this.dom_.getElement('btn-search'),
      goog.events.EventType.CLICK, goog.events.Event.preventDefault);

  this.eh_.listen(this.dom_.getElement('btn-submit'),
      goog.events.EventType.CLICK, this.onSubmit_, false, this);

  this.eh_.listen(this.dom_.getElement('btn-pass'),
      goog.events.EventType.CLICK, this.onPass_, false, this);

  this.eh_.listen(this.ac_, goog.ui.AutoComplete.EventType.SUGGESTIONS_UPDATE,
      this.onAcUpdate_, false, this);

};


/**
 * Clear the form.
 */
ffc.quiz.AnswerForm.prototype.clearForm = function() {
  this.ac_.dismiss(true);
  this.acInput_.value = '';
  this.suggestInfo_.style.display = 'block';
};


/**
 * Handle clicking the clear button.
 * @param {goog.events.Event} e The browser event.
 * @private.
 */
ffc.quiz.AnswerForm.prototype.onClear_ = function(e) {
  this.clearForm();
  e.preventDefault();
};


/**
 * Handle auto complete update.
 * @param {goog.events.Event} e The autocomplete update event.
 * @private
 */
ffc.quiz.AnswerForm.prototype.onAcUpdate_ = function(e) {
  if (e.target.rows_.length) {
    this.suggestInfo_.style.display = 'none';
  } else {
    this.suggestInfo_.style.display = 'block';
  }
};


/**
 * Handle clicking the 'Pass' button.
 * @param {goog.events.Event} e The browser event.
 * @private
 */
ffc.quiz.AnswerForm.prototype.onPass_ = function(e) {
  this.submitGuess_(ffc.quiz.AnswerForm.PASS_);
  e.preventDefault();
};


/**
 * Handle clicking the 'Submit' button.
 * @param {goog.events.Event} e The browser event.
 * @private
 */
ffc.quiz.AnswerForm.prototype.onSubmit_ = function(e) {
  var formDataMap = goog.dom.forms.getFormDataMap(this.element_);
  var answer = formDataMap.get('answer') && formDataMap.get('answer')[0];

  if (answer) {
    this.submitGuess_(answer);
  }

  e.preventDefault();
};


/**
 * Submit a guess.
 * @param {string} guess The users guess.
 * @private
 */
ffc.quiz.AnswerForm.prototype.submitGuess_ = function(guess) {
  goog.net.XhrIo.send('/api' + window.location.pathname + '?guess=' + guess,
      goog.bind(this.onGuessResponse_, this));
};


/**
 * Handle a response form the server after making a guess.
 * @param {goog.events.Event} e The xhr event.
 * @private
 */
ffc.quiz.AnswerForm.prototype.onGuessResponse_ = function(e) {
  var data = e.target.getResponseJson();
  this.dispatchEvent(
      new ffc.quiz.AnswerFormEvent(
          ffc.quiz.AnswerForm.ANSWER_RESPONSE, this, data));
};


/**
 * The Answer response event.
 * @type {string}
 */
ffc.quiz.AnswerForm.ANSWER_RESPONSE = 'answerresponseevent';


/**
 * A special string to send the server as a guess when the user passes.
 * @private
 */
ffc.quiz.AnswerForm.PASS_ = 'pass';



/**
 * Object representing an answer form event.
 * @param {string} type The event type.
 * @param {ffc.quiz.AnswerForm} target The event target.
 * @param {Object} data
 *     {Array.<Object>} clues
 *       {string?} image The path to the image clue.
 *       {string?} text The text for the clue.
 *     {boolean} complete
 *     {boolean} correct
 *     {Array.<Object>} guesses
 *       {string?} title The title of the film guess.
 *       {string?} year The year of the film guess.
 * @extends {goog.events.Event}
 * @constructor
 */
ffc.quiz.AnswerFormEvent = function(type, target, data) {
  goog.base(this, type, target);

  /**
   * @type {Object}
   */
  this.data = data;
};
goog.inherits(ffc.quiz.AnswerFormEvent, goog.events.Event);
