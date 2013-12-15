// Copyright 2011 Friday Film Club All Rights Reserved.

/**
 * @fileoverview The leaderboard view/controller.
 *
 * @author adamjmcgrath@gmail.com (Adam Mcgrath)
 */

goog.provide('ffc.leaderboard.LeaderBoard');

goog.require('ffc.leaderboard.LeaderBoardModel');
goog.require('ffc.template.leaderboard');

goog.require('goog.array');
goog.require('goog.dom');
goog.require('goog.dom.classes');
goog.require('goog.dom.TagName');
goog.require('goog.string');
goog.require('goog.ui.Component');
goog.require('goog.uri.utils');

goog.require('soy');



/**
 * LeaderBoard constructor.
 * @param {ffc.leaderboard.LeaderBoardModel} model The leaderboard model.
 * @constructor
 */
ffc.leaderboard.LeaderBoard = function(model) {
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

  this.setModel(model);
};
goog.inherits(ffc.leaderboard.LeaderBoard, goog.ui.Component);
goog.exportSymbol('ffc.leaderboard.LeaderBoard', ffc.leaderboard.LeaderBoard);
goog.exportProperty(ffc.leaderboard.LeaderBoard.prototype, 'render',
    ffc.leaderboard.LeaderBoard.prototype.render);


/**
 * @return {string} The type of leaderboard, 'all' or 'week'.
 */
ffc.leaderboard.LeaderBoard.prototype.getType = function() {
  return this.model_.id;
};


/**
 * @override
 */
ffc.leaderboard.LeaderBoard.prototype.createDom = function() {
  var el = this.dh_.createDom(goog.dom.TagName.DIV);
  this.dh_.append(el, soy.renderAsElement(ffc.template.leaderboard.table));
  this.dh_.append(el,
      soy.renderAsElement(ffc.template.leaderboard.pagination));
  this.decorateInternal(el);
};


/**
 * @override
 */
ffc.leaderboard.LeaderBoard.prototype.decorateInternal = function(el) {
  goog.base(this, 'decorateInternal', el);
  this.tBodyEl_ = this.getElementByClass('leaderboard-users');
  this.paginationEl_ = this.getElementByClass('pagination');
};


/**
 * @override
 */
ffc.leaderboard.LeaderBoard.prototype.enterDocument = function() {
  goog.base(this, 'enterDocument');

  this.model_.subscribe(ffc.leaderboard.LeaderBoardModel.TOTAL_UPDATED_EVENT,
      this.fillPagination_, this);
  this.model_.subscribe(ffc.leaderboard.LeaderBoardModel.USERS_UPDATED_EVENT,
      this.fillLeaderBoard_, this);

  this.eh_.listen(this.paginationEl_, goog.events.EventType.CLICK,
      this.handlePaginationClick_, true, this);

  this.model_.getData();

  this.element_.style.display = 'block';
  goog.dom.classes.add(this.element_, 'loading');
};


/**
 * @override
 */
ffc.leaderboard.LeaderBoard.prototype.exitDocument = function() {
  goog.base(this, 'exitDocument');

  this.model_.clear();
  this.eh_.removeAll();

  this.dh_.removeChildren(this.element_);
  this.element_ = null;
};


/**
 * @private
 */
ffc.leaderboard.LeaderBoard.prototype.fillLeaderBoard_ = function() {
  this.dh_.removeChildren(this.tBodyEl_);
  var args = [this.tBodyEl_];
  var users = this.model_.users;
  var TagName = goog.dom.TagName;
  for (var i = 0, len = users.length; i < len; i++) {
    var user = users[i];
    args.push(this.dh_.createDom(TagName.TR, null,
        this.dh_.createDom(TagName.TD, null,
            this.dh_.createDom(TagName.IMG, user.picAttrs())),
        this.dh_.createDom(TagName.TD, null,
          this.dh_.createDom(TagName.A, {href: '/u/' + user.name}, user.name)),
        this.dh_.createDom(TagName.TD, 'leaderboard-clues', user.clues + ''),
        this.dh_.createDom(TagName.TD, 'leaderboard-score', user.score + ''),
        this.dh_.createDom(TagName.TD, 'leaderboard-answered', user.answered + ''),
        this.dh_.createDom(TagName.TD, 'leaderboard-averageclues', user.averageClues() + ''),
        this.dh_.createDom(TagName.TD, 'leaderboard-average', user.averageScore() + '')));
  }
  goog.dom.classes.remove(this.element_, 'loading');
  this.dh_.append.apply(this._dh, args);
};


/**
 * @private
 */
ffc.leaderboard.LeaderBoard.prototype.fillPagination_ = function() {
  this.dh_.removeChildren(this.paginationEl_);
  var args = [this.paginationEl_];
  var pages = goog.array.range(
      Math.ceil(this.model_.totalScores / this.model_.pageSize));

  // Only make pagination if >1 page.
  if (!(pages.length > 1)) {
    return;
  }
  for (var i = 0, len = pages.length; i < len; i++) {
    args.push(soy.renderAsElement(ffc.template.leaderboard.page,
        {number: pages[i] + 1, active: i == this.model_.page}));
  }
  this.dh_.append.apply(this._dh, args);
};


/**
 * @param {goog.events.Event} e The click event.
 * @private
 */
ffc.leaderboard.LeaderBoard.prototype.handlePaginationClick_ = function(e) {
  e.preventDefault();
  if (e.target.nodeName == goog.dom.TagName.A) {
    // Display page numbers are 1 indexed.
    var pageNumber = parseInt(e.target.innerHTML, 10) - 1;
    if (pageNumber != this.model_.page) {
      this.model_.page = pageNumber;
      this.model_.getData();
    }
  }
};

