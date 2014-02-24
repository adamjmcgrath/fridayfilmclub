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
goog.require('goog.fx.Transition.EventType');

goog.require('grow.fx.dom.Shake');

goog.require('soy');



/**
 * Answer form constructor.
 * @constructor
 */
ffc.quiz.AnswerForm = function() {
  goog.base(this);

  this.eh_ = this.getHandler();

  /**
   * The auto complete.
   * @type {ffc.suggest.AutoComplete}
   * @private
   */
  this.ac_ = null;

  /**
   * The incorrect shake animation.
   * @type {grow.fx.dom.Shake}
   * @private
   */
  this.shake_ = null;

  /**
   * The place older element for an empty list of suggestions
   * @type {Element}
   * @private
   */
  this.suggestInfo_ = null;

  /**
   * The input to deocrate with the autocomplete.
   * @type {Element}
   * @private
   */
  this.acInput_ = null;
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
      this.getElementByClass('suggestions'), 'answer');

  this.eh_.listen(this.dom_.getElement('btn-clear'),
      goog.events.EventType.CLICK, this.onClear_);

  this.eh_.listen(this.dom_.getElement('btn-search'),
      goog.events.EventType.CLICK, goog.events.Event.preventDefault);

  this.eh_.listen(this.dom_.getElement('btn-submit'),
      goog.events.EventType.CLICK, this.onSubmit_, false, this);

  this.eh_.listen(this.dom_.getElement('btn-pass'),
      goog.events.EventType.CLICK, this.onPass_, false, this);

  this.eh_.listen(this.ac_, goog.ui.ac.AutoComplete.EventType.SUGGESTIONS_UPDATE,
      this.onAcUpdate_, false, this);

  this.shake_ = new grow.fx.dom.Shake(this.element_);

};


/**
 * Clear the form.
 * @param {function() {}} callback A function to call once the shake
 *     animation has finished.
 */
ffc.quiz.AnswerForm.prototype.showIncorrect = function(callback) {
  this.clearForm();
  this.eh_.listenOnce(this.shake_, goog.fx.Transition.EventType.END, callback);
  this.shake_.play();
};


/**
 * Show a loading indicator.
 * @param {boolean} isLoading
 */
ffc.quiz.AnswerForm.prototype.setLoading = function(isLoading) {
  goog.dom.classes.enable(this.element_, 'is-loading', !!isLoading)
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
  this.suggestInfo_.style.display = e.target.rows_.length ? 'none' : 'block';
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
 * Change the answer form to reflect that it is the users last guess.
 */
ffc.quiz.AnswerForm.prototype.setLastGuess = function() {
  var passBtn = this.dom_.getElement('btn-pass');
  if (passBtn) {
    passBtn.innerHTML = 'No idea, I give up';
  }
};


/**
 * Submit a guess.
 * @param {string} guess The users guess.
 * @private
 */
ffc.quiz.AnswerForm.prototype.submitGuess_ = function(guess) {
  this.dispatchEvent(new ffc.quiz.AnswerFormEvent(
      ffc.quiz.AnswerForm.MAKE_GUESS, this, guess));
};


/**
 * @override
 */
ffc.quiz.AnswerForm.prototype.disposeInternal = function(guess) {
  goog.base(this, 'disposeInternal');
  this.shake_.dispose();
  this.ac_.dispose();
  this.shake_ = null;
  this.suggestInfo_ = null;
  this.acInput_ = null;
};


/**
 * The guess event.
 * @type {string}
 */
ffc.quiz.AnswerForm.MAKE_GUESS = 'makeguessevent';


/**
 * A special string to send the server as a guess when the user passes.
 * @private
 */
ffc.quiz.AnswerForm.PASS_ = 'pass';



/**
 * Object representing an answer form event.
 * @param {string} type The event type.
 * @param {ffc.quiz.AnswerForm} target The event target.
 * @param {string} guess The user's guess (or 'pass').
 * @extends {goog.events.Event}
 * @constructor
 */
ffc.quiz.AnswerFormEvent = function(type, target, guess) {
  goog.base(this, type, target);

  /**
   * @type {string}
   */
  this.guess = guess;
};
goog.inherits(ffc.quiz.AnswerFormEvent, goog.events.Event);
