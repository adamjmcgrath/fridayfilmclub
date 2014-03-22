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
goog.require('goog.ds.SortedNodeList');
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
  this.pages = 0;

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
 * The value of the last user on the previous page.
 * @type {number}
 */
ffc.leaderboard.LeaderBoardModel.prototype.previousValue = null;


/**
 * The value of the first user on the next page.
 * @type {number}
 */
ffc.leaderboard.LeaderBoardModel.prototype.nextValue = null;


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

  this.previousValue = data['prev'];
  this.nextValue = data['next'];

  this.totalScores = data['count'];
  this.pages = Math.ceil(this.totalScores / this.pageSize);
  this.publish(ffc.leaderboard.LeaderBoardModel.TOTAL_UPDATED_EVENT);

  this.users = new goog.ds.SortedNodeList(this.getCompareFn(),
      goog.array.map(data['users'], ffc.api.User.build));

  this.publish(ffc.leaderboard.LeaderBoardModel.USERS_UPDATED_EVENT);
};


/**
 * @return {Function} A compare function based on the current sort and direction.
 */
ffc.leaderboard.LeaderBoardModel.prototype.getCompareFn = function() {
  var sort = this.sortField,
      dir = this.sortDir;
  return function(a, b) {
    a = a.getChildNodeValue(sort);
    b = b.getChildNodeValue(sort);
    if (dir == 'asc') {
      return goog.array.defaultCompare(a, b);
    } else {
      return goog.array.defaultCompare(b, a);
    }
  };
};

/**
 * @param {ffc.api.User} newUser The user instance.
 */
ffc.leaderboard.LeaderBoardModel.prototype.insertUser = function(newUser) {
  var isAsc = this.sortDir == 'asc',
      isLastPage = this.isLastPage(),
      prev = this.page > 0 ? this.previousValue : isAsc ? 0 : Infinity,
      next = !isLastPage ? this.nextValue : isAsc ? Infinity : 0,
      range = [prev, next],
      min = Math.min.apply(Math, range),
      max = Math.max.apply(Math, range),
      value = newUser.getChildNodeValue(this.sortField),
      remove;

  if (min <= value && value <= max) {
    this.users.removeNode(newUser.getDataName());
    this.users.add(newUser);

    // Move the last user to a new page if users > page size. Add a new page if
    // on the last page.
    remove = this.users.getByIndex(this.pageSize);
    if (remove) {
      this.users.removeNode(remove.getDataName());
      if (isLastPage) {
        this.pages++;
        this.publish(ffc.leaderboard.LeaderBoardModel.TOTAL_UPDATED_EVENT);
      }
    }

    this.publish(ffc.leaderboard.LeaderBoardModel.USERS_UPDATED_EVENT);
  }

};

/**
 * @return {boolean} If on last page.
 */
ffc.leaderboard.LeaderBoardModel.prototype.isLastPage = function() {
  return this.page == this.pages - 1;
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
