// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview The leaderboard model, holds the scores.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.leaderboard.LeaderBoardModel');

goog.require('ffc.api.Client');
goog.require('ffc.api.User');

goog.require('goog.Uri');
goog.require('goog.array');
goog.require('goog.pubsub.PubSub');



/**
 * Leaderboard model.
 * @param {string} id The leaderboard id.
 * @param {ffc.api.Client} client The REST client.
 * @constructor
 */
ffc.leaderboard.LeaderBoardModel = function(id, client) {
  goog.base(this);

  /**
   * @type {string}
   */
  this.id = id;

  /**
   * @type {number}
   */
  this.page = 0;

  /**
   * @type {number}
   */
  this.pageSize = ffc.leaderboard.LeaderBoardModel.DEFAULT_PAGE_SIZE_;

  /**
   * @type {string}
   */
  this.sortField = ffc.leaderboard.LeaderBoardModel.DEFAULT_SORT;

  /**
   * @type {string}
   */
  this.sortDir = ffc.leaderboard.LeaderBoardModel.DEFAULT_DIR;

  /**
   * @type {Function}
   * @private
   */
  this.getData_ = goog.bind(client.getLeaderBoard, client, id);
};
goog.inherits(ffc.leaderboard.LeaderBoardModel, goog.pubsub.PubSub);
goog.exportSymbol('ffc.leaderboard.LeaderBoardModel',
    ffc.leaderboard.LeaderBoardModel);


/**
 * Get a new page of scores.
 */
ffc.leaderboard.LeaderBoardModel.prototype.getData = function() {
  this.getData_(this.page * this.pageSize, this.pageSize,
      this.sortField, this.sortDir).wait(this.handleResult.bind(this));
};


/**
 * Sort the leaderboard.
 * @param {string} sort The sort field.
 * @param {string} dir The direction 'asc' or 'dsc'.
 */
ffc.leaderboard.LeaderBoardModel.prototype.sort = function(sort, dir) {
  this.sortField = sort;
  this.sortDir = dir;
  this.getData();
};


/**
 * @param {goog.result.Result} result The ajax result.
 */
ffc.leaderboard.LeaderBoardModel.prototype.handleResult = function(result) {
  var data = result.getValue();

  this.totalScores = data['count'];
  this.publish(ffc.leaderboard.LeaderBoardModel.TOTAL_UPDATED_EVENT);

  this.users = goog.array.map(data['users'], ffc.api.User.build);
  this.publish(ffc.leaderboard.LeaderBoardModel.USERS_UPDATED_EVENT);
};


/**
 * The different types of leaderboard.
 * @enum {string}
 */
ffc.leaderboard.LeaderBoardModel.Type = {
  ALL: 'all',
  WEEK: 'week'
};


/**
 * @type {Number}
 * @private
 */
ffc.leaderboard.LeaderBoardModel.DEFAULT_PAGE_SIZE_ = 20;


/**
 * @type {string}
 */
ffc.leaderboard.LeaderBoardModel.USERS_UPDATED_EVENT = 'usersUpdated';


/**
 * @type {string}
 */
ffc.leaderboard.LeaderBoardModel.TOTAL_UPDATED_EVENT = 'totalUpdated';


/**
 * @type {string}
 */
ffc.leaderboard.LeaderBoardModel.DEFAULT_SORT = 'score';


/**
 * @type {string}
 */
ffc.leaderboard.LeaderBoardModel.DEFAULT_DIR = 'dsc';
