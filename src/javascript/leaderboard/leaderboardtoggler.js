// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview The leader board toggler.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.leaderboard.LeaderBoardToggler');

goog.require('goog.dom.TagName');
goog.require('goog.dom.classes');
goog.require('goog.dom.dataset');



/**
 * LeaderBoardToggler constructor.
 * @param {ffc.leaderboard.LeaderBoard} var_args Some leaderboards.
 *
 * @constructor
 */
ffc.leaderboard.LeaderBoardToggler = function(var_args) {
  goog.base(this);

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

  /**
   * @type {Array.<ffc.leaderboard.LeaderBoard>}
   * @private
   */
  this.leaderBoards_ = Array.prototype.slice.call(arguments, 0);

};
goog.inherits(ffc.leaderboard.LeaderBoardToggler, goog.ui.Component);
goog.exportSymbol('ffc.leaderboard.LeaderBoardToggler',
    ffc.leaderboard.LeaderBoardToggler);
goog.exportProperty(ffc.leaderboard.LeaderBoardToggler.prototype, 'decorate',
    ffc.leaderboard.LeaderBoardToggler.prototype.decorate);


/**
 * @override
 */
ffc.leaderboard.LeaderBoardToggler.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');

  this.eh_.listen(this.element_, goog.events.EventType.CLICK,
      this.handleTabClick_, true, this);
};


/**
 * @param {goog.events.Event} e The click event.
 * @private
 */
ffc.leaderboard.LeaderBoardToggler.prototype.handleTabClick_ = function(e) {
  e.preventDefault();
  var li = this.dh_.getAncestorByTagNameAndClass(e.target, goog.dom.TagName.LI);
  var cls = 'active';
  if (e.target.nodeName == goog.dom.TagName.A && li &&
      !goog.dom.classes.has(li, cls)) {
    var type = goog.dom.dataset.get(e.target, 'leaderboard');
    goog.dom.classes.remove(
        this.dh_.getElementByClass(cls, this.element_), cls);
    goog.dom.classes.add(li, cls);
    for (var i = 0, len = this.leaderBoards_.length; i < len; i++) {
      var lb = this.leaderBoards_[i];
      if (lb.getType() == type) {
        lb.render();
      } else {
        lb.exitDocument();
      }
    }
  }
};


/**
 * @override
 */
ffc.leaderboard.LeaderBoardToggler.prototype.disposeInternal = function(e) {
  goog.base(this, 'disposeInternal');
};
