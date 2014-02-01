// @ use_closure_library=true
// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Auto complete for Movies data.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.invite.AutoComplete');
goog.provide('ffc.invite.AutoComplete.Event');

goog.require('ffc.api.Client');
goog.require('ffc.invite.GoogleRow');
goog.require('ffc.invite.FacebookRow');
goog.require('ffc.invite.TwitterRow');
goog.require('ffc.invite.InputHandler');

goog.require('goog.array');
goog.require('goog.dom');
goog.require('goog.dom.classes');
goog.require('goog.dom.dataset');
goog.require('goog.object');
goog.require('goog.ui.ac.AutoComplete');
goog.require('goog.ui.ac.ArrayMatcher');
goog.require('goog.ui.ac.Renderer');



/**
 * AutoComplete constructor.
 * @param {HTMLInputElement} el The input element to decorate.
 * @param {string} provider 'google','facebook' or 'twitter'
 * @param {Element} parent The element to render the autocomplete list in.
 * @param {HTMLInputElement} valueInput Stores the values.
 * @constructor
 */
ffc.invite.AutoComplete = function(el, provider, parent, valueInput) {

  /**
   * The main input element.
   * @type {HTMLInputElement}
   * @private
   */
  this.element_ = el;

  /**
   * The main container.
   * @type {HTMLElement}
   * @private
   */
  this.container_ = goog.dom.getAncestorByTagNameAndClass(el,
      null, 'input-group');

  /**
   * The value input.
   * @type {HTMLElement}
   * @private
   */
  this.valueInput_ = valueInput;

  /**
   * 'google','facebook' or 'twitter'.
   * @type {string}
   * @private
   */
  this.provider_ = provider;

  /**
   * @type {Object.<string, ffc.invite.AbstractRow>}
   * @private
   */
  this.selectedRows_ = {};

  /**
   * A standard renderer that uses a custom row renderer to display the
   * rich rows generated by this autocomplete widget.
   * @type {goog.ui.AutoComplete.Renderer}
   * @private
   */
  this.renderer_ = new goog.ui.ac.Renderer(parent);

  /**
   * A matcher the takes a uri to a suggest endpoint and returns an object to
   * use in the renderer.
   * @type {goog.ui.ac.ArrayMatcher}
   * @private
   */
  this.matcher_ = new goog.ui.ac.ArrayMatcher();

  var inputHandler = new ffc.invite.InputHandler(
      null, ',', true, 300);

  goog.ui.ac.AutoComplete.call(this, this.matcher_,
      this.renderer_, inputHandler);

  inputHandler.attachAutoComplete(this);
  inputHandler.attachInputs(el);
  inputHandler.setSeparatorSelects(false);

  ffc.api.Client.getInstance()
                .getContacts(provider)
                .wait(this.handleContactsResponse_, this);

  this.setLoading(true);

  goog.events.listen(this.container_, 'click', this.handleClick_, null, this);
};
goog.inherits(ffc.invite.AutoComplete, goog.ui.ac.AutoComplete);
goog.exportSymbol('ffc.invite.AutoComplete', ffc.invite.AutoComplete);


/**
 * @param {Object} response
 * @private
 */
ffc.invite.AutoComplete.prototype.handleContactsResponse_ = function(response) {
  var values = response.getValue(),
      rows = [],
      i, len, row;

  for (i = 0, len = values.length; i < len; i++) {
    row = ffc.invite.AutoComplete.Row_[this.provider_].fromRowData(values[i]);
    row.subscribe(ffc.invite.AbstractRow.Event.SELECTED,
        this.handleRowSelected_, this);
    rows[i] = row;
  }
  this.matcher_.setRows(rows);
  this.setLoading(false);
};


/**
 * @param {boolean} isLoading
 */
ffc.invite.AutoComplete.prototype.setLoading = function(isLoading) {
  goog.dom.classes.enable(this.container_, 'loading', !!isLoading);
};


/**
 * @param {ffc.invite.AbstractRow} row
 */
ffc.invite.AutoComplete.prototype.selectRow = function(row) {
  this.handleRowSelected_(row);
};


/**
 * @param {ffc.invite.AbstractRow} row
 */
ffc.invite.AutoComplete.prototype.handleRowSelected_ = function(row) {
  goog.dom.insertSiblingBefore(row.getSelectedDom(), this.element_);
  this.selectedRows_[row.id] = row;
  this.dispatchEvent(ffc.invite.AutoComplete.Event.ITEM_SELECTED);
  this.element_.value = '';
  this.updateValueInput();
};


/**
 * @param {goog.events.Event} e
 */
ffc.invite.AutoComplete.prototype.handleClick_ = function(e) {
  if (goog.dom.classes.has(e.target, 'remove')) {
    var dom = goog.dom.getAncestorByClass(e.target, 'contact'),
        id = goog.dom.dataset.get(dom, 'row');
    delete this.selectedRows_[id];
    dom.remove();
    this.dispatchEvent(ffc.invite.AutoComplete.Event.ITEM_REMOVED);
    this.updateValueInput();
  }
};


/**
 * Upadate the hidden value input.
 */
ffc.invite.AutoComplete.prototype.updateValueInput = function() {
  this.valueInput_.value = this.getValue().join(',');
};


/**
 * @param {boolean} enable
 */
ffc.invite.AutoComplete.prototype.enable = function(enable) {
  if (enable) {
    this.element_.removeAttribute('disabled');
  } else {
    this.element_.setAttribute('disabled', 'disabled');
  }
  goog.dom.classes.enable(this.container_, 'disabled', !enable);
};


/**
 * @param {goog.events.Event} e
 */
ffc.invite.AutoComplete.prototype.getValue = function(e) {
  return goog.object.getKeys(goog.object.filter(this.selectedRows_,
      function(row) {
        return !row.isInvalidEmail;
      }
    )
  );
};

/**
 * @enum {String}
 */
ffc.invite.AutoComplete.Row_ = {
  'google': ffc.invite.GoogleRow,
  'facebook': ffc.invite.FacebookRow,
  'twitter': ffc.invite.TwitterRow
};


/**
 * @enum {String}
 */
ffc.invite.AutoComplete.Event = {
  ITEM_REMOVED: 'item_removed',
  ITEM_SELECTED: 'item_selected'
};
