// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Realtime scores component.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.quiz.RealtimeScores');


goog.require('goog.dom');
goog.require('goog.fx.dom.FadeOutAndHide');
goog.require('goog.i18n.NumberFormat');
goog.require('goog.i18n.NumberFormat.Format');
goog.require('goog.json');
goog.require('ffc.template.quiz');

goog.require('soy');


/**
 * Realtime scores constructor.
 * @param {String} channelToken Token for the Channel API.
 * @param {Element} container
 * @constructor
 */
ffc.quiz.RealtimeScores = function(channelToken, container) {
  var channel = new appengine.Channel(channelToken),
      socket = channel.open();
  socket.onmessage = this.onMessage_.bind(this);
  this.formatter_ = new goog.i18n.NumberFormat(
      goog.i18n.NumberFormat.Format.DECIMAL);
  this.element_ = container;
};
goog.exportSymbol('ffc.quiz.RealtimeScores', ffc.quiz.RealtimeScores);


/**
 * Handle the Channel message.
 * @param {Object} msg
 * @private
 */
ffc.quiz.RealtimeScores.prototype.onMessage_ = function(msg) {
  var msgObj = goog.json.parse(msg['data']),
      scoreDom = soy.renderAsFragment(ffc.template.quiz.realtimeScore, {
    user: msgObj['user'],
    pic: msgObj['pic'],
    score: this.formatter_.format(msgObj['score'])
  }),
      lastScore = goog.dom.getFirstElementChild(this.element_),
      fx;

  // Insert the score.
  if (lastScore) {
    goog.dom.insertSiblingBefore(scoreDom, lastScore);
  } else {
    goog.dom.appendChild(this.element_, scoreDom);
  }

  // Wait then fade out the score.
  fx = new goog.fx.dom.FadeOutAndHide(scoreDom, 300);
  setTimeout(fx.play.bind(fx), ffc.quiz.RealtimeScores.TIMEOUT);

};

/**
 * The length of time in ms to show a score.
 * @type {number}
 */
ffc.quiz.RealtimeScores.TIMEOUT = 6 * 1000;

