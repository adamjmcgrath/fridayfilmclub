// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview FFC api client.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.api.Client');

goog.require('goog.labs.net.xhr');
goog.require('goog.result.Result');



/**
 * Api rest client constructor.
 * @constructor
 */
ffc.api.Client = function() {
};
goog.addSingletonGetter(ffc.api.Client);
goog.exportSymbol('ffc.api.Client.getInstance', ffc.api.Client.getInstance);


/**
 * Get.
 * @param {string} url The URL to request.
 * @param {Object=} opt_options Configuration options for the request.
 * @return {goog.result.Result} A result object that will be resolved
 *     with the response text once the request finishes.
 * @private
 */
ffc.api.Client.prototype.get_ = function(url, opt_options) {
  return goog.labs.net.xhr.getJson.apply(null, arguments);
};


/**
 * Post.
 * @param {string} url The URL to request.
 * @param {Object} data The body of the post request.
 * @param {Object=} opt_options Configuration options for the request.
 * @return {goog.result.Result} A result object that will be resolved
 *     with the response text once the request finishes.
 * @private
 */
ffc.api.Client.prototype.post_ = function(url, data, opt_options) {
  return goog.labs.net.xhr.post.apply(null, arguments);
};


/**
 * @param {string} type Should be 'all' or 'week', for all time and this week.
 * @param {number=} opt_page The page number.
 * @param {number=} opt_pageSize The page size.
 * @param {string=} opt_sort The sort field.
 * @param {string=} opt_dir The direction: asc or dsc.
 * @return {goog.result.Result} The ajax result.
 */
ffc.api.Client.prototype.getLeaderBoard = function(type,
    opt_page, opt_pageSize, opt_sort, opt_dir) {
  var uri = goog.Uri.parse(
      goog.string.subs(ffc.api.Client.LEADER_BOARD_PATH_, type));

  if (opt_page) {
    uri.setParameterValue('offset', opt_page);
  }
  if (opt_pageSize) {
    uri.setParameterValue('limit', opt_pageSize);
  }
  if (opt_sort) {
    uri.setParameterValue('sort', opt_sort);
  }
  if (opt_dir) {
    uri.setParameterValue('dir', opt_dir);
  }

  return this.get_(uri);
};


/**
 * @type {string}
 * @private
 */
ffc.api.Client.BASE_PATH_ = '/api';


/**
 * @type {string}
 * @private
 */
ffc.api.Client.QUESTION_PATH_ = ffc.api.Client.BASE_PATH_ + '/question';


/**
 * @type {string}
 * @private
 */
ffc.api.Client.LEADER_BOARD_PATH_ =
    ffc.api.Client.BASE_PATH_ + '/leaderboard/%s';
