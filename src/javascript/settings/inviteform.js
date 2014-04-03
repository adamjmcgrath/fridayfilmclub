// Copyright 2012 Friday Film Club All Rights Reserved.

/**
 * @fileoverview An invite form.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
goog.provide('ffc.settings.InviteForm');

goog.require('ffc.quiz.Component');

goog.require('goog.dom');
goog.require('goog.dom.classes');
goog.require('goog.dom.forms');
goog.require('goog.events.EventType');
goog.require('goog.net.XhrIo');
goog.require('goog.string');



/**
 * Invite form constructor.
 * @constructor
 */
ffc.settings.InviteForm = function(model) {
  goog.base(this);
};
goog.inherits(ffc.settings.InviteForm, ffc.quiz.Component);
goog.exportSymbol('ffc.settings.InviteForm', ffc.settings.InviteForm);
goog.exportProperty(ffc.settings.InviteForm.prototype, 'decorate',
    ffc.settings.InviteForm.prototype.decorate);


/**
 * @override
 */
ffc.settings.InviteForm.prototype.decorateInternal = function(el) {
  goog.base(this, 'decorateInternal', el);

  this.numInvites_ = goog.dom.getElementByClass('num-invites',
      this.element_);

  this.emailField_ = goog.dom.getElementByClass('invite-email',
      this.element_);
};


/**
 * @override
 */
ffc.settings.InviteForm.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');
  var eh = this.getHandler();

  eh.listen(this.element_, goog.events.EventType.SUBMIT,
        this.onSubmit_, false, this);
};


/**
 * Populate the autocomplete dataset.
 */
ffc.settings.InviteForm.prototype.populateAutoComplete = function() {
    goog.net.XhrIo.send(ffc.settings.InviteForm.GOOGLE_CONTACTS_URL_,
      this.onEmailsResponse_.bind(this));
};
goog.exportProperty(ffc.settings.InviteForm.prototype, 'populateAutoComplete',
    ffc.settings.InviteForm.prototype.populateAutoComplete);


/**
 * @param {goog.events.Event} e
 */
ffc.settings.InviteForm.prototype.onSubmit_ = function(e) {
  e.preventDefault();

  if (this.disabled_) {
    return;
  }
  this.disabled_ = true;

  goog.dom.classes.remove(this.element_, ffc.settings.InviteForm.ERROR_CLS_);

  var data = goog.dom.forms.getFormDataString(this.element_);

  goog.net.XhrIo.send(ffc.settings.InviteForm.URL_,
      this.onResponse_.bind(this), 'POST', data);

  window['ga'] && window['ga']('send', 'event', 'invite', 'send',
      goog.dom.forms.getValueByName(this.element_, 'email'));
};


/**
 * @param {goog.events.Event} e
 */
ffc.settings.InviteForm.prototype.onResponse_ = function(e) {
  var response = e.target.getResponseJson();

  if (response['success']) {
    this.numInvites_.innerHTML = response['invites'];
    goog.dom.forms.setValue(this.emailField_, '');
  } else {
    goog.dom.classes.add(this.element_, ffc.settings.InviteForm.ERROR_CLS_);
  }
  this.disabled_ = false;
};


/**
 * @param {goog.events.Event} e
 */
ffc.settings.InviteForm.prototype.onEmailsResponse_ = function(e) {
  var contacts = e.target.getResponseJson(),
      datalist = document.getElementById('emailAutoComplete'),
      tpl = '<option value="%s" label="%s" />',
      html = [],
      contact, i, len;

  for (i = 0, len = contacts.length; i < len; i++) {
    contact = contacts[i];
    html[i] = goog.string.subs(tpl, contact['email'], contact['name']);
  }

  datalist.innerHTML = html.join('');
};


/**
 * @type {string}
 */
ffc.settings.InviteForm.URL_ = '/sendinvite_legacy';


/**
 * @type {string}
 */
ffc.settings.InviteForm.GOOGLE_CONTACTS_URL_ = '/api/contacts/google';


/**
 * @type {string}
 */
ffc.settings.InviteForm.ERROR_CLS_ = 'has-error';