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
 * @type {boolean}
 */
ffc.leaderboard.User.prototype.isAdmin = null;


/**
 * @type {string}
 */
ffc.leaderboard.User.prototype.pic = null;


/**
 * @type {number}
 */
ffc.leaderboard.User.prototype.answered = null;


/**
 * @type {string}
 */
ffc.leaderboard.User.prototype.score = null;


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
 * @return {number} The average score over all games played.
 */
ffc.leaderboard.User.prototype.averageScore = function() {
  return (this.score / this.answered).toFixed(1) || 0;
};


/**
 * @param {Object} jsonObj Response from the REST api.
 * @return {ffc.leaderboard.User} A user instance.
 */
ffc.leaderboard.User.build = function(jsonObj) {
  var user = new ffc.leaderboard.User();
  user.name = jsonObj['user_name'];
  user.isAdmin = jsonObj['is_admin'];
  user.pic = jsonObj['user_pic'];
  user.score = jsonObj['score'];
  user.answered = jsonObj['answered'];
  return user;
};
