// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 *
 * <div class="clue">
 *   <p><b>Clue #:</b> Clue text.</p>
 * </div>
 * 
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
goog.provide('ffc.Clue');

goog.require('goog.dom');
goog.require('goog.dom.TagName');
goog.require('goog.fx.dom.FadeInAndShow');
goog.require('goog.string');
goog.require('goog.style');



/**
 * Clue constructor.
 * @constructor
 */
ffc.Clue = function(number, text) {

  /**
   * The number of the clue.
   * @type {number}
   */
  this.number = number;

  /**
   * @type {string}
   */
  this.text = text;

};


/**
 *
 */
ffc.Clue.CLASS_NAME = 'clue';


/**
 *
 */
ffc.Clue.TPL = '<p><b>Clue %s:</b> %s</p>';


/**
 *
 */
ffc.Clue.prototype.render = function(parent) {
  var container = goog.dom.createDom(goog.dom.TagName.DIV,
      ffc.Clue.CLASS_NAME);

  container.innerHTML = goog.string.subs(ffc.Clue.TPL, this.number,
      goog.string.htmlEscape(this.text));

  parent.appendChild(container);
  (new goog.fx.dom.FadeInAndShow(container, 500)).play();
};
