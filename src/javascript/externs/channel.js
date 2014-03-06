/**
 * @fileoverview Externs for App Engine Channel API client library.
 *
 * @see https://developers.google.com/appengine/docs/python/channel/javascript
 * @externs
 */

/**
 * Use appengine rather than goog, see:
 * https://groups.google.com/d/msg/closure-compiler-discuss/Z8sThaEEb34/UA75Xdi1fDoJ
 * @type {Object}
 * @const
 */
var appengine = {};

/**
 * @param {string} token
 * @constructor
 */
appengine.Channel = function(token) {};

/**
 * @param {Object=} opt_handler
 */
appengine.Channel.prototype.open = function(opt_handler) {};


/**
 * @constructor
 */
appengine.Socket = function() {};

/**
 * @type {Function}
 */
appengine.Socket.prototype.onopen;

/**
 * @type {Function}
 */
appengine.Socket.prototype.onmessage;

/**
 * @type {Function}
 */
appengine.Socket.prototype.onerror;

/**
 * @type {Function}
 */
appengine.Socket.prototype.onclose;

