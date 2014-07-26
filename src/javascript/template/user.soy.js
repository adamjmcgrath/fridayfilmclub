// This file was automatically generated from user.soy.
// Please don't edit this file by hand.

goog.provide('ffc.template.user');

goog.require('soy');
goog.require('soydata');


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.user.searchResult = function(opt_data, opt_ignored) {
  return '<span>' + ((opt_data.pic) ? '<img src="' + soy.$$escapeHtml(opt_data.pic) + '">' : '') + '<span class="name">' + soy.$$escapeHtml(opt_data.username) + ' (' + soy.$$escapeHtml(opt_data.name) + ')</span></span>';
};
