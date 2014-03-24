// @ use_closure_library=true
// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Request invite modal.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.invite.ModalPopup');

goog.require('ffc.template.requestinvite');
goog.require('goog.dom.classes');
goog.require('goog.dom.forms');
goog.require('goog.events');
goog.require('goog.events.EventType');
goog.require('goog.format.EmailAddress');
goog.require('goog.net.XhrIo');
goog.require('goog.style');
goog.require('goog.ui.Dialog');



/**
 * Request an invite modal popup constructor.
 * @constructor
 */
ffc.invite.ModalPopup = function(btn) {
  goog.base(this);

  this.btn_ = btn;

  /**
   * Event handler for this object.
   * @type {goog.events.EventHandler}
   * @private
   */
  this.eh_ = this.getHandler();

  /**
   * The dom helper.
   * @type {goog.dom.DomHelper}
   * @private
   */
  this.dh_ = this.getDomHelper();

  this.init();
};
goog.inherits(ffc.invite.ModalPopup, goog.ui.Dialog);
goog.exportSymbol('ffc.invite.ModalPopup', ffc.invite.ModalPopup);


/**
 * @type {Element}
 * @private
 */
ffc.invite.ModalPopup.prototype.validationMsg_ = null;


/**
 * @type {Element}
 * @private
 */
ffc.invite.ModalPopup.prototype.inviteForm_ = null;


/**
 * @type {Element}
 * @private
 */
ffc.invite.ModalPopup.prototype.emailField_ = null;


/**
 * @type {Element}
 * @private
 */
ffc.invite.ModalPopup.prototype.btn_ = null;


/**
 * Add the behaviour the the button.
 */
ffc.invite.ModalPopup.prototype.init = function() {
  goog.events.listen(this.btn_, goog.events.EventType.CLICK,
      this.onBtnClick_, null, this);
  this.setTitle('Request an Invite');
  this.setButtonSet(null);
  goog.dom.classes.add(this.getTitleCloseElement(),
    'glyphicon glyphicon-remove');
};


/**
 * Show/hide the validation message.
 */
ffc.invite.ModalPopup.prototype.setValid = function(isValid) {
  goog.style.setElementShown(this.validationMsg_, !isValid);
};


/**
 * @inheritDocs
 */
ffc.invite.ModalPopup.prototype.onShow = function() {
  goog.base(this, 'onShow');

  this.setContent(ffc.template.requestinvite.form());

  this.validationMsg_ = this.dh_.getElementByClass('validation-message');
  this.inviteForm_ = this.dh_.getElementByClass('request-invite-form');
  this.emailField_ = this.dh_.getElementByClass('email-field');

  this.eh_.listen(this.inviteForm_, goog.events.EventType.SUBMIT,
      this.onInviteFormSubmit_, null, this);

  this.setValid(true);
  goog.dom.forms.setValue(this.emailField_, '');
};


/**
 * Add the behaviour the the button.
 */
ffc.invite.ModalPopup.prototype.onBtnClick_ = function(e) {
  e.preventDefault();
  this.setVisible(true);
};


/**
 * Add the behaviour the the button.
 */
ffc.invite.ModalPopup.prototype.onInviteFormSubmit_ = function(e) {
  e.preventDefault();
  var email = goog.dom.forms.getValueByName(e.target, 'email'),
      isValid = goog.format.EmailAddress.isValidAddress(email);
  if (isValid) {
    goog.net.XhrIo.send(ffc.invite.ModalPopup.REQUEST_INVITE_URL_,
        goog.bind(this.onRequestInviteResponse_, this),
        'POST',
        'email=' + email);
  }
  this.setValid(isValid);
};


/**
 * Add the behaviour the the button.
 */
ffc.invite.ModalPopup.prototype.onRequestInviteResponse_ = function(e) {
  var sentTo = e.target.getResponseJson()['sent_to'];
  if (sentTo) {
    this.setContent(ffc.template.requestinvite.message({
      email: sentTo
    }));
  }
  this.setValid(!!sentTo);
};


/**
 * @type {string}
 */
ffc.invite.ModalPopup.REQUEST_INVITE_URL_ = '/requestinvite';