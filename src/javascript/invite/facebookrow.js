// @ use_closure_library=true
// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete Google row.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.invite.FacebookRow');

goog.require('ffc.template.contacts');

goog.require('goog.dom');
goog.require('goog.dom.TagName');
goog.require('ffc.invite.AbstractRow');
goog.require('goog.string');

goog.require('soy');



/**
 * Google Row constructor.
 * @param {String} name
 * @param {String} id
 * @param {String} pic
 * @constructor
 */
ffc.invite.FacebookRow = function(name, id, pic) {
  goog.base(this);
  this.name = name;
  this.id = id;
  this.pic = pic;
};
goog.inherits(ffc.invite.FacebookRow, ffc.invite.AbstractRow);


/**
 * @return {HTMLElement}
 */
ffc.invite.FacebookRow.prototype.createDom = function() {
  return soy.renderAsElement(ffc.template.contacts.contact, {
    name: this.name,
    img: this.pic,
    id: this.id
  })
};


/**
 * @inheritDocs
 */
ffc.invite.FacebookRow.prototype.toString = function() {
   return this.name;
};


/**
 * @param {Object} rowData
 */
ffc.invite.FacebookRow.fromRowData = function(rowData) {
  return new ffc.invite.FacebookRow(rowData['name'],
      rowData['username'] || rowData['id'],
      'http://graph.facebook.com/' + rowData['id'] + '/picture');
};