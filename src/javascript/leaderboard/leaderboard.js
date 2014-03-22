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
goog.require('goog.dom.dataset');
goog.require('goog.dom.TagName');
goog.require('goog.string');
goog.require('goog.ui.Component');
goog.require('goog.uri.utils');

goog.require('soy');



/**
 * LeaderBoard constructor.
 * @param {ffc.leaderboard.LeaderBoardModel} model The leaderboard model.
 * @param {String} opt_channelToken Token for the Channel API.
 * @constructor
 */
ffc.leaderboard.LeaderBoard = function(model, opt_channelToken) {
  goog.base(this);

  if (opt_channelToken) {
    var channel = new appengine.Channel(opt_channelToken),
      socket = channel.open();
    socket.onmessage = this.onMessage_.bind(this);
  }

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
 * @type {ffc.leaderboard.LeaderBoardModel}
 * @private
 */
ffc.leaderboard.LeaderBoard.prototype.model_ = null;


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
  this.eh_.listen(this.element_, goog.events.EventType.CLICK,
      this.handleMainClick_, true, this);

  this.model_.sort('score', 'dsc');

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
  var args = [this.tBodyEl_],
      users = this.model_.users,
      TagName = goog.dom.TagName,
      i, len;
  for (i = 0, len = users.getCount(); i < len; i++) {
    var user = users.getByIndex(i);
    args.push(this.dh_.createDom(TagName.TR, null,
        this.dh_.createDom(TagName.TD, null, this.dh_.createDom(TagName.IMG, user.picAttrs())),
        this.dh_.createDom(TagName.TD, null, this.dh_.createDom(TagName.A, {href: '/u/' + user.getDataName()}, user.getDataName())),
        this.dh_.createDom(TagName.TD, 'leaderboard-clues', user.getChildNodeValue('clues') + ''),
        this.dh_.createDom(TagName.TD, 'leaderboard-score', user.getScore() + ''),
        this.dh_.createDom(TagName.TD, 'leaderboard-answered', user.getChildNodeValue('answered') + ''),
        this.dh_.createDom(TagName.TD, 'leaderboard-averageclues', user.averageClues() + ''),
        this.dh_.createDom(TagName.TD, 'leaderboard-average', user.averageScore() + '')));
  }
  goog.dom.classes.remove(this.element_, 'loading');
  this.dh_.append.apply(this.dh_, args);
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


/**
 * @param {goog.events.Event} e The click event.
 * @private
 */
ffc.leaderboard.LeaderBoard.prototype.handleMainClick_ = function(e) {
  var TH = goog.dom.TagName.TH,
      th = goog.dom.getAncestorByTagNameAndClass(e.target, TH),
      sort = th && goog.dom.dataset.get(th, 'sort');
  if (sort) {
    var dir = goog.dom.classes.has(th, 'asc') ? 'dsc' : 'asc';
    var ths = goog.dom.getElementsByTagNameAndClass(TH, null, this.element_);
    goog.array.forEach(ths, function(thitem) {
      goog.dom.classes.remove(thitem, 'asc');
      goog.dom.classes.remove(thitem, 'dsc');
    });
    goog.dom.classes.add(th, dir);
    this.model_.sort(sort, dir);
  }
};


/**
 * Handle the Channel message.
 * @param {Object} msg
 *   {string} user
 *   {string} pic
 *   {number} score Score for this week.
 *   {number} clues Clues used this week.
 *   {number} season_score Score this season.
 *   {number} season_clues Clues used this season.
 *   {number} season_answered Questions answered this season.
 *   {number} all_score All time score.
 *   {number} all_clues All time clues used.
 *   {number} all_answered All time questions answered.
 * @private
 */
ffc.leaderboard.LeaderBoard.prototype.onMessage_ = function(msg) {
  if (!this.isInDocument()) {
    return;
  }
  var msgObj = goog.json.parse(msg['data']),
      score, clues, answered, user;

  if (this.getType() == ffc.leaderboard.LeaderBoard.Type.WEEK) {
    score = msgObj['score'];
    clues = msgObj['clues'];
  } else if (this.getType() == ffc.leaderboard.LeaderBoard.Type.ALL) {
    score = msgObj['all_score'];
    clues = msgObj['all_clues'];
    answered = msgObj['all_answered'];
  } else {
    score = msgObj['season_score'];
    clues = msgObj['season_clues'];
    answered = msgObj['season_answered'];
  }

  user = ffc.api.User.buildFromRealtimeMessage(msgObj, score, clues, answered);
  this.model_.insertUser(user);
};


/**
 * Leaderboard types.
 * @enum {string}
 */
ffc.leaderboard.LeaderBoard.Type = {
  WEEK: 'week',
  ALL: 'all'
};
