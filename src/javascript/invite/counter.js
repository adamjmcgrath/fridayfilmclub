// @ use_closure_library=true
// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview Invite counter.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.invite.Counter');

goog.require('goog.array');
goog.require('goog.events');
goog.require('ffc.invite.AutoComplete.Event');



/**
 * AutoComplete constructor.
 * @constructor
 */
ffc.invite.Counter = function(numInvites, dom, acs) {
  this.dom_ = dom;
  this.acs_ = acs;

  this.setCount(numInvites);

  goog.array.forEach(this.acs_, this.decorateAc_, this);
};


/**
 * Set the count
 * @param {number} count
 */
ffc.invite.Counter.prototype.setCount = function(count) {
  this.count_ = count;
  this.dom_.innerHTML = count;
  this.acs_.forEach(function(ac) {
    ac.enable(!!count);
  });
};


/**
 * Increment count.
 */
ffc.invite.Counter.prototype.incrementCount = function() {
  this.setCount(this.count_ + 1);
};


/**
 * Increment count.
 */
ffc.invite.Counter.prototype.decrementCount = function() {
  this.setCount(Math.max(this.count_ - 1, 0));
};


/**
 * Add listeners to the auto complete.
 * @param {ffc.invite.AutoComplete} ac
 */
ffc.invite.Counter.prototype.decorateAc_ = function(ac) {
  goog.events.listen(ac, ffc.invite.AutoComplete.Event.ITEM_SELECTED,
      this.decrementCount, null, this);
  goog.events.listen(ac, ffc.invite.AutoComplete.Event.ITEM_REMOVED,
      this.incrementCount, null, this);
};
