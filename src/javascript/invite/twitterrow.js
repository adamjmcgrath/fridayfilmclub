// @ use_closure_library=true
// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete Google row.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.invite.TwitterRow');

goog.require('ffc.template.contacts');

goog.require('goog.dom');
goog.require('goog.dom.TagName');
goog.require('ffc.invite.AbstractRow');
goog.require('goog.string');

goog.require('soy');



/**
 * Twitter Row constructor.
 * @param {String} name
 * @param {String} id
 * @param {String} pic
 * @constructor
 */
ffc.invite.TwitterRow = function(name, id, pic) {
  goog.base(this);
  this.name = name;
  this.id = id;
  this.pic = pic;
};
goog.inherits(ffc.invite.TwitterRow, ffc.invite.AbstractRow);


/**
 * @return {HTMLElement}
 */
ffc.invite.TwitterRow.prototype.createDom = function() {
  return soy.renderAsElement(ffc.template.contacts.contact, {
    name: this.toString(),
    img: this.pic,
    id: this.id
  })
};


/**
 * @inheritDocs
 */
ffc.invite.TwitterRow.prototype.toString = function() {
  var name;
  if (this.id != this.name) {
    name = this.name + ' (@' + this.id + ')';
  } else {
    name = '@' + this.name;
  }
 return name;
};

/**
 * @param {Object} rowData
 */
ffc.invite.TwitterRow.fromRowData = function(rowData) {
  return new ffc.invite.TwitterRow(rowData['name'], rowData['id'],
      rowData['pic']);
};