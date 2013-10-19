// This file was automatically generated from leaderboard.soy.
// Please don't edit this file by hand.

goog.provide('ffc.template.leaderboard');

goog.require('soy');
goog.require('soydata');


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.leaderboard.table = function(opt_data, opt_ignored) {
  return '<table class="table table-striped table-hover"><thead><tr><th colspan="2">User</th><th class="leaderboard-score">Score</th><th class="leaderboard-answered">Answered</th><th class="leaderboard-average">Av. Score</th></tr></thead><tbody class="leaderboard-users"></tbody></table>';
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.leaderboard.pagination = function(opt_data, opt_ignored) {
  return '<div class="leaderboard-pagination"><ul class="pagination pagination-sm"></ul></div>';
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.leaderboard.page = function(opt_data, opt_ignored) {
  return '<li' + ((opt_data.active) ? ' class="active"' : '') + '><a href="#">' + soy.$$escapeHtml(opt_data.number) + '</a></li>';
};
