// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview The user table model.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.league.UsersModel');

goog.require('ffc.api.User');

goog.require('goog.array');
goog.require('goog.ds.SortedNodeList');
goog.require('goog.pubsub.PubSub');



/**
 * Users table model.
 * @constructor
 */
ffc.league.UsersModel = function() {
  goog.base(this);

  this.users_ = new goog.ds.SortedNodeList(
      ffc.league.UsersModel.reverse)
};
goog.inherits(ffc.league.UsersModel, goog.pubsub.PubSub);
goog.exportSymbol('ffc.league.UsersModel', ffc.league.UsersModel);


/**
 * @type {goog.ds.SortedNodeList}
 */
ffc.league.UsersModel.prototype.users_ = null;


/**
 * @param {Object[]} data
 */
ffc.league.UsersModel.prototype.addUserData = function(data) {
  for (var i = 0, userData; userData = data[i]; i++) {
    this.addUser(ffc.api.User.buildFromUserData(userData), true);
  }

  this.publish(ffc.league.UsersModel.USERS_UPDATED_EVENT);
};


/**
 * @param {ffc.api.User} user
 * @param {boolean} silent Suppress the event.
 */
ffc.league.UsersModel.prototype.addUser = function(user, silent) {
  this.users_.add(user);
  if (!silent) {
    this.publish(ffc.league.UsersModel.USERS_UPDATED_EVENT);
  }
};


/**
 * @param {string} userName
 * @param {boolean} silent Suppress the event.
 */
ffc.league.UsersModel.prototype.removeUser = function(userName, silent) {
  this.users_.removeNode(userName);
  if (!silent) {
    this.publish(ffc.league.UsersModel.USERS_UPDATED_EVENT);
  }
};


/**
 * @return {goog.ds.SortedNodeList}
 */
ffc.league.UsersModel.prototype.getUsers = function() {
  return this.users_;
};


/**
 * @return {string[]}
 */
ffc.league.UsersModel.prototype.getKeys = function() {
  var keys = [];
  for (var i = 0, len = this.users_.getCount(); i < len; i++) {
    keys[i] = this.users_.getByIndex(i).key;
  }
  return keys;
};

/**
 * @type {string}
 */
ffc.league.UsersModel.USERS_UPDATED_EVENT = 'usersUpdated';


/**
 * A reverse function.
 * @return {number}
 */
ffc.league.UsersModel.reverse = function() {
   return -1;
};