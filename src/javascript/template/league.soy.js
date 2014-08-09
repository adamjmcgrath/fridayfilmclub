// This file was automatically generated from league.soy.
// Please don't edit this file by hand.

goog.provide('ffc.template.league');

goog.require('soy');
goog.require('soydata');


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.league.userTable = function(opt_data, opt_ignored) {
  var output = '';
  var userList36 = opt_data.list_;
  var userListLen36 = userList36.length;
  if (userListLen36 > 0) {
    for (var userIndex36 = 0; userIndex36 < userListLen36; userIndex36++) {
      var userData36 = userList36[userIndex36];
      output += '<tr><td><img src="' + soy.$$escapeHtml(userData36.pic) + '" alt="' + soy.$$escapeHtml(userData36.name) + '" width="20" height="20"></td><td><a href="/u/' + soy.$$escapeHtml(userData36.name) + '">' + soy.$$escapeHtml(userData36.name) + '</a></td><td><button type="button" class="btn btn-default btn-xs" data-remove-user="' + soy.$$escapeHtml(userData36.name) + '"><span class="glyphicon glyphicon-remove"></span> Remove</button></td></tr>';
    }
  } else {
    output += '<tr><td colspan="3" class="empty">Add a user</td></tr>';
  }
  return output;
};
