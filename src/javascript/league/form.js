// Copyright Friday Film Club All Rights Reserved.

/**
 * @fileoverview The add/edit league form.
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */
goog.provide('ffc.league.Form');

goog.require('ffc.template.league');
goog.require('ffc.api.User');


goog.require('goog.events');
goog.require('goog.ui.Component');
goog.require('goog.ui.ac.AutoComplete.EventType');

goog.require('soy');


/**
 * Answer constructor.
 * @param {ffc.league.UsersModel} usersModel The users data.
 * @param {ffc.usersuggest.AutoComplete} autoComplete The users suggest field.
 * @constructor
 */
ffc.league.Form = function(usersModel, autoComplete) {
  goog.base(this);

  this.usersModel_ = usersModel;
  this.autoComplete_ = autoComplete;
};
goog.inherits(ffc.league.Form, goog.ui.Component);
goog.exportSymbol('ffc.league.Form', ffc.league.Form);


/**
 * @type {ffc.league.UsersModel}
 * @private
 */
ffc.league.Form.prototype.usersModel_ = null;


/**
 * @type {ffc.usersuggest.AutoComplete}
 * @private
 */
ffc.league.Form.prototype.autoComplete_ = null;


/**
 * @type {HTMLButtonElement}
 * @private
 */
ffc.league.Form.prototype.addUserBtn_ = null;


/**
 * @type {ffc.api.User}
 * @private
 */
ffc.league.Form.prototype.selectedUser_ = null;


/**
 * @param {HTMLFormElement} el
 */
ffc.league.Form.prototype.decorateInternal = function(el) {
  goog.base(this, 'decorateInternal', el);
  this.addUserBtn_ = this.getElementByClass('add-user');
  this.userTable_ = this.getElementByClass('league-users');
  this.userKeysField_ = this.getElementByClass('user-keys');
};


/**
 * @override
 */
ffc.league.Form.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');

  this.usersModel_.subscribe(ffc.league.UsersModel.USERS_UPDATED_EVENT,
      this.fillUserTable_, this);

  goog.events.listen(this.autoComplete_,
      goog.ui.ac.AutoComplete.EventType.UPDATE, this.onUserSelected_, false,
      this);

  goog.events.listen(this.getElement(), goog.events.EventType.SUBMIT,
      this.onFormSubmitted_, false, this);

  goog.events.listen(this.addUserBtn_, goog.events.EventType.CLICK,
      this.onAddUserClick_, false, this);
};


/**
 * Set selected user state.
 * @param {goog.events.Event} e
 */
ffc.league.Form.prototype.onUserSelected_ = function(e) {
  this.selectedUser_ = ffc.api.User.buildFromUserSearch(e.row);
};


/**
 * Set selected user state.
 * @param {goog.events.Event} e
 */
ffc.league.Form.prototype.onAddUserClick_ = function(e) {
  var users = this.usersModel_.getUsers();
  if (this.selectedUser_ &&
      !goog.isDef(users.indexOf(this.selectedUser_['name']))) {
    this.usersModel_.addUser(this.selectedUser_);
    this.selectedUser_ = null;
    this.autoComplete_.getTarget().value = '';
  }
};


/**
 * Populate the user table.
 */
ffc.league.Form.prototype.fillUserTable_ = function() {
  soy.renderElement(this.userTable_, ffc.template.league.userTable,
        this.usersModel_.getUsers());
};


/**
 * Serialize the mode and add the values to the form.
 * @param {goog.events.Event} e
 */
ffc.league.Form.prototype.onFormSubmitted_ = function(e) {
  this.userKeysField_.value = this.usersModel_.getKeys().join(',');
};
