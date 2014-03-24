// This file was automatically generated from requestinvite.soy.
// Please don't edit this file by hand.

goog.provide('ffc.template.requestinvite');

goog.require('soy');
goog.require('soydata');


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.requestinvite.form = function(opt_data, opt_ignored) {
  return '<form action="" method="post" class="request-invite-form clearfix"><div class="form-group"><small class="text-danger pull-right validation-message">Please enter a valid email.</small><input class="form-control email-field" name="email" placeholder="you@example.com" type="text" value="" /></div><div><button type="submit" class="btn btn-primary pull-right send-request">Send Request</button></div></form>';
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.requestinvite.message = function(opt_data, opt_ignored) {
  return '<div class="alert alert-success"><p>An invite has been sent to <strong>' + soy.$$escapeHtml(opt_data.email) + '</strong>.</p><p>Open the email and follow the instructions to join.</p><p>Welcome to the Friday Film Club!</p></div>';
};
