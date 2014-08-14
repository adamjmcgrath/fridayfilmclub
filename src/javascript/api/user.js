// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview A leader board user model.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.api.User');

goog.require('goog.ds.FastDataNode');
goog.require('goog.i18n.NumberFormat');
goog.require('goog.i18n.NumberFormat.Format');


/**
 * A user object.
 * @param {string} name
 * @param {string} pic
 * @param {number} score
 * @param {number} clues
 * @param {number} answered
 * @param {string} realName
 * @param {string} key
 * @constructor
 */
ffc.api.User = function(name, pic, score, clues, answered, realName, key) {
    this.floatFormatter_ = new goog.i18n.NumberFormat('#,##0.0');
    this.intFormatter_ = new goog.i18n.NumberFormat(
      goog.i18n.NumberFormat.Format.DECIMAL);
    goog.base(this, {
      'name': name,
      'realName': realName,
      'pic': pic,
      'score': score,
      'clues': clues,
      'answered': answered,
      'key': key
    }, name);
};
goog.inherits(ffc.api.User, goog.ds.FastDataNode);

/**
 * @type {goog.i18n.NumberFormat}
 */
ffc.api.User.prototype.formatter_ = null;

/**
 * @return {Object} The attributes to display an image element.
 */
ffc.api.User.prototype.picAttrs = function() {
  return {
    src: this.getChildNodeValue('pic'),
    alt: this.getDataName(),
    width: 20,
    height: 20
  };
};


/**
 * @return {string} The average score over all games played.
 */
ffc.api.User.prototype.getScore = function() {
  return this.intFormatter_.format(this.getChildNodeValue('score'));
};


/**
 * @return {string} The average score over all games played.
 */
ffc.api.User.prototype.averageScore = function() {
  return this.floatFormatter_.format(
      (this.getChildNodeValue('score') / this.getChildNodeValue('answered')) || 0);
};


/**
 * @return {string} The average clues used over all games played.
 */
ffc.api.User.prototype.averageClues = function() {
  return this.floatFormatter_.format(
      (this.getChildNodeValue('clues') / this.getChildNodeValue('answered')) || 0);
};


/**
 * @param {Object} obj Response from the REST api.
 * @return {ffc.api.User} A user instance.
 */
ffc.api.User.build = function(obj) {
  return new ffc.api.User(obj['user_name'],
                          obj['user_pic'],
                          obj['score'],
                          obj['clues'],
                          obj['answered']);
};


/**
 * @param {Object} obj Response from the REST api.
 * @param {number} score
 * @param {number} clues
 * @param {number} answered
 * @return {ffc.api.User} A user instance.
 */
ffc.api.User.buildFromRealtimeMessage = function(obj, score, clues, answered) {
  var user = new ffc.api.User(obj['user'],
                              obj['pic'],
                              score,
                              clues,
                              answered);
  user.setChildNode('live', true);
  return user;
};


/**
 * @param {Object} obj Response from the REST api.
 * @return {ffc.api.User} A user instance.
 */
ffc.api.User.buildFromUserSearch = function(obj) {
  var user = new ffc.api.User(obj['username'],
                              obj['pic'],
                              null,
                              null,
                              null,
                              obj['name'],
                              obj['key']);
  user.setChildNode('live', true);
  return user;
};


/**
 * @param {Object} obj User object from inline json on league page.
 * @return {ffc.api.User} A user instance.
 */
ffc.api.User.buildFromUserData = function(obj) {
  return new ffc.api.User(obj['username'],
                          obj['pic'],
                          null,
                          null,
                          null,
                          obj['name'],
                          obj['key']);
};