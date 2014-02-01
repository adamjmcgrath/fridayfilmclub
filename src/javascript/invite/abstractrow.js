// @ use_closure_library=true
// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete Google row.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.invite.AbstractRow');

goog.require('goog.pubsub.PubSub');


/**
 * AutoComplete constructor.
 * @constructor
 */
ffc.invite.AbstractRow = function() {
  goog.base(this);
  this.dom_ = null;
};
goog.inherits(ffc.invite.AbstractRow, goog.pubsub.PubSub);


/**
 * @return {String}
 */
ffc.invite.AbstractRow.prototype.getId = function() {
  return this.id;
};


/**
 * Create a string representation of the row for searching.
 */
ffc.invite.AbstractRow.prototype.toString = goog.abstractMethod;


/**
 * Create the row dom.
 */
ffc.invite.AbstractRow.prototype.createDom = goog.abstractMethod;


/**
 * Get the selected row dom.
 */
ffc.invite.AbstractRow.prototype.getSelectedDom = function() {
  this.dom_ = this.dom_ || this.createDom();
  return this.dom_;
};


/**
 * Handle the select event.
 * @param {HTMLElement} inputEl
 */
ffc.invite.AbstractRow.prototype.select = function(inputEl) {
  this.publish(ffc.invite.AbstractRow.Event.SELECTED, this);
};


/**
 * Factory method to create a new row.
 * @param {Object} rowData
 */
ffc.invite.AbstractRow.fromRowData = goog.abstractMethod;


/**
 * @enum {String}
 */
ffc.invite.AbstractRow.Event = {
  SELECTED: 'selected'
};