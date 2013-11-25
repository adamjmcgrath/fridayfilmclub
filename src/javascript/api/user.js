// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview A leader board user model.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.api.User');



/**
 * User constructor.
 * @constructor
 */
ffc.api.User = function() {
};


/**
 * @type {string}
 */
ffc.api.User.prototype.name = null;


/**
 * @type {string}
 */
ffc.api.User.prototype.pic = null;


/**
 * @type {number}
 */
ffc.api.User.prototype.answered = null;


/**
 * @type {number}
 */
ffc.api.User.prototype.score = null;


/**
 * @type {number}
 */
ffc.api.User.prototype.clues = null;


/**
 * @return {Object} The attributes to display an image element.
 */
ffc.api.User.prototype.picAttrs = function() {
  return {
    src: this.pic,
    alt: this.name,
    width: 20,
    height: 20
  };
};


/**
 * @return {string} The average score over all games played.
 */
ffc.api.User.prototype.averageScore = function() {
  return ((this.score / this.answered)|| 0).toFixed(1);
};


/**
 * @return {string} The average clues used over all games played.
 */
ffc.api.User.prototype.averageClues = function() {
  return ((this.clues / this.answered)|| 0).toFixed(1);
};


/**
 * @param {Object} jsonObj Response from the REST api.
 * @return {ffc.api.User} A user instance.
 */
ffc.api.User.build = function(jsonObj) {
  var user = new ffc.api.User();
  user.name = jsonObj['user_name'];
  user.pic = jsonObj['user_pic'];
  user.score = jsonObj['score'];
  user.answered = jsonObj['answered'];
  user.clues = jsonObj['clues'];
  return user;
};
