// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview A leader board user model.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.leaderboard.User');



/**
 * User constructor.
 * @constructor
 */
ffc.leaderboard.User = function() {
};


/**
 * @type {string}
 */
ffc.leaderboard.User.prototype.name = null;


/**
 * @type {string}
 */
ffc.leaderboard.User.prototype.pic = null;


/**
 * @type {number}
 */
ffc.leaderboard.User.prototype.answered = null;


/**
 * @type {number}
 */
ffc.leaderboard.User.prototype.score = null;


/**
 * @type {number}
 */
ffc.leaderboard.User.prototype.clues = null;


/**
 * @return {Object} The attributes to display an image element.
 */
ffc.leaderboard.User.prototype.picAttrs = function() {
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
ffc.leaderboard.User.prototype.averageScore = function() {
  return ((this.score / this.answered)|| 0).toFixed(1);
};


/**
 * @return {string} The average clues used over all games played.
 */
ffc.leaderboard.User.prototype.averageClues = function() {
  return ((this.clues / this.answered)|| 0).toFixed(1);
};


/**
 * @param {Object} jsonObj Response from the REST api.
 * @return {ffc.leaderboard.User} A user instance.
 */
ffc.leaderboard.User.build = function(jsonObj) {
  var user = new ffc.leaderboard.User();
  user.name = jsonObj['user_name'];
  user.pic = jsonObj['user_pic'];
  user.score = jsonObj['score'];
  user.answered = jsonObj['answered'];
  user.clues = jsonObj['clues'];
  return user;
};
