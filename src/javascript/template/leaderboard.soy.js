// This file was automatically generated from leaderboard.soy.
// Please don't edit this file by hand.

goog.provide('ffc.template.leaderboard');

goog.require('soy');
goog.require('soy.StringBuilder');


/**
 * @param {Object.<string, *>=} opt_data
 * @param {soy.StringBuilder=} opt_sb
 * @return {string}
 * @notypecheck
 */
ffc.template.leaderboard.table = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<table class="table table-striped table-hover"><thead><tr><th colspan="2">User</th><th class="leaderboard-number">Score</th><th class="leaderboard-number">Answered</th><th class="leaderboard-number">Av. Score</th></tr></thead><tbody class="leaderboard-users"></tbody></table>');
  return opt_sb ? '' : output.toString();
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {soy.StringBuilder=} opt_sb
 * @return {string}
 * @notypecheck
 */
ffc.template.leaderboard.pagination = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<div class="leaderboard-pagination"><ul class="pagination pagination-sm"></ul></div>');
  return opt_sb ? '' : output.toString();
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {soy.StringBuilder=} opt_sb
 * @return {string}
 * @notypecheck
 */
ffc.template.leaderboard.page = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<li', (opt_data.active) ? ' class="active"' : '', '><a href="#">', soy.$$escapeHtml(opt_data.number), '</a></li>');
  return opt_sb ? '' : output.toString();
};
