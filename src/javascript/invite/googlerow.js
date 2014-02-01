// @ use_closure_library=true
// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete Google row.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.invite.GoogleRow');

goog.require('ffc.template.contacts');

goog.require('goog.dom');
goog.require('goog.dom.TagName');
goog.require('ffc.invite.AbstractRow');
goog.require('goog.string');

goog.require('soy');



/**
 * Google Row constructor.
 * @param {String} name
 * @param {String} email
 * @param {String} pic
 * @constructor
 */
ffc.invite.GoogleRow = function(name, email, pic) {
  goog.base(this);
  this.name = name;
  this.email = this.id = email;
  this.pic = pic;
};
goog.inherits(ffc.invite.GoogleRow, ffc.invite.AbstractRow);


/**
 * @return {HTMLElement}
 */
ffc.invite.GoogleRow.prototype.createDom = function() {
  return soy.renderAsElement(ffc.template.contacts.contact, {
    name: this.name,
    img: this.pic,
    id: this.id
  })
};


/**
 *
 */
ffc.invite.GoogleRow.prototype.toString = function() {
   return goog.string.subs('%s <%s>', this.name, this.email);
};

/**
 *
 * @param {Object} rowData
 */
ffc.invite.GoogleRow.fromRowData = function(rowData) {
  return new ffc.invite.GoogleRow(rowData['name'], rowData['email'],
      rowData['pic']);
};