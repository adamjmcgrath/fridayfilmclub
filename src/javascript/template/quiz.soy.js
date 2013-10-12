// This file was automatically generated from quiz.soy.
// Please don't edit this file by hand.

goog.provide('ffc.template.quiz');

goog.require('soy');
goog.require('soy.StringBuilder');


/**
 * @param {Object.<string, *>=} opt_data
 * @param {soy.StringBuilder=} opt_sb
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.answerForm = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<form class="well answer-form"><div class="form-inline"><div class="input-group"><span class="input-group-addon">Search</span><input class="autocomplete input-lg form-control" size="16" type="text" autocomplete="off"></div><a href="#" class="btn btn-lg btn-success" id="btn-search">Search</a><a href="#" class="btn btn-lg btn-warning" id="btn-clear">Clear</a></div><div class="controls rows"><div class="suggestions"><p class="suggest-info">Search for a film, then select your guess from the list.</p></div></div><div class="guess-buttons"><a href="#" class="btn btn-primary" id="btn-submit">Submit</a><a href="#" class="btn btn-danger" id="btn-pass">Pass</a></div></form>');
  return opt_sb ? '' : output.toString();
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {soy.StringBuilder=} opt_sb
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.option = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<label class="radio', (opt_data.odd) ? ' odd' : '', '"><input type="radio" name="answer" value="', soy.$$escapeHtml(opt_data.key), '">', soy.$$escapeHtml(opt_data.title), '<span>', soy.$$escapeHtml(opt_data.year), '</span></label>');
  return opt_sb ? '' : output.toString();
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {soy.StringBuilder=} opt_sb
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.guess = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<div class="alert alert-warning failed-guess">', (opt_data.title) ? '<b>' + soy.$$escapeHtml(opt_data.title) + ' (' + soy.$$escapeHtml(opt_data.year) + ')</b> is incorrect!' : '<b>PASS</b>', '</div>');
  return opt_sb ? '' : output.toString();
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {soy.StringBuilder=} opt_sb
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.clue = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<div class="', (opt_data.image) ? 'thumbnail' : 'alert alert-info clue', '">', (opt_data.image) ? '<img src="' + soy.$$escapeHtml(opt_data.image) + '" width="910" height="343"><div class="caption"><h4>Clue #' + soy.$$escapeHtml(opt_data.position) + '</h4>' + ((opt_data.text) ? '<p>' + soy.$$escapeHtml(opt_data.text) + '</p>' : '') + '</div>' : (opt_data.text) ? '<p><b>Clue #' + soy.$$escapeHtml(opt_data.position) + ': </b>' + soy.$$escapeHtml(opt_data.text) + '</p>' : '', '</div>');
  return opt_sb ? '' : output.toString();
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {soy.StringBuilder=} opt_sb
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.answer = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<div class="alert alert-', (opt_data.correct) ? 'success' : 'danger', ' clue"><h4 class="alert-heading">', (opt_data.correct) ? 'Correct!' : 'Incorrect!', '</h4><p>The answer is of course: <b>', soy.$$escapeHtml(opt_data.title), '</b> (', soy.$$escapeHtml(opt_data.year), ')</p></div>');
  return opt_sb ? '' : output.toString();
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {soy.StringBuilder=} opt_sb
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.score = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<div class="well score"><h4>Points available:</h4><p class="points-available">');
  var sList91 = opt_data.score;
  var sListLen91 = sList91.length;
  for (var sIndex91 = 0; sIndex91 < sListLen91; sIndex91++) {
    var sData91 = sList91[sIndex91];
    output.append('<span class="point">', soy.$$escapeHtml(sData91), '</span>');
  }
  output.append('<sub></sub></p><h4>Clues:</h4><div class="progress"><div class="bar bar-active bar-1">1</div><div class="bar', (opt_data.clueCount > 1) ? ' bar-active' : '', ' bar-2">2</div><div class="bar', (opt_data.clueCount > 2) ? ' bar-active' : '', ' bar-3">3</div><div class="bar', (opt_data.clueCount > 3) ? ' bar-active' : '', ' bar-4">4</div></div></div>');
  return opt_sb ? '' : output.toString();
};
