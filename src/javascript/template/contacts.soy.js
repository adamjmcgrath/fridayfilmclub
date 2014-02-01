// This file was automatically generated from contacts.soy.
// Please don't edit this file by hand.

goog.provide('ffc.template.contacts');

goog.require('soy');
goog.require('soydata');


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.contacts.contact = function(opt_data, opt_ignored) {
  return '<span class="contact' + ((opt_data.cls) ? ' ' + soy.$$escapeHtml(opt_data.cls) : '') + '" data-row="' + soy.$$escapeHtml(opt_data.id) + '">' + ((opt_data.img) ? '<img src="' + soy.$$escapeHtml(opt_data.img) + '">' : '') + '<span class="name">' + soy.$$escapeHtml(opt_data.name) + '</span><span class="glyphicon glyphicon-remove remove"></span></span>';
};
