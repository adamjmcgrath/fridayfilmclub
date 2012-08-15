// Copyright 2012 Friday Film Club All Rights Reserved.

/**
 * @fileoverview A base component class, handles items fading in
 * on entering document.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
goog.provide('ffc.quiz.Component');

goog.require('goog.fx.dom.FadeInAndShow');
goog.require('goog.ui.Component');



/**
 * Base component condsructor.
 * @constructor
 */
ffc.quiz.Component = function() {
  goog.base(this);
};
goog.inherits(ffc.quiz.Component, goog.ui.Component);


/**
 * Base component condsructor.
 * @type {goog.fx.dom.FadeInAndShow}
 * @private
 */
ffc.quiz.Component.prototype.fx_ = null;


/**
 * Fade the root element in when adding it to the document.
 */
ffc.quiz.Component.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');

  this.fx_ = new goog.fx.dom.FadeInAndShow(
      this.element_, ffc.quiz.Component.FADE_DELAY_);
  this.fx_.play();
};


/**
 * Disposes of the animation.
 */
ffc.quiz.Component.prototype.disposeInternal = function() {
  this.fx_.destroy();
  goog.base(this, 'disposeInternal');
};


/**
 * Fade in time.
 * @type {string}
 * @private
 */
ffc.quiz.Component.FADE_DELAY_ = 500;
