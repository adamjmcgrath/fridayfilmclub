// This file was automatically generated from quiz.soy.
// Please don't edit this file by hand.

goog.provide('ffc.template.quiz');

goog.require('soy');
goog.require('soydata');


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.answerForm = function(opt_data, opt_ignored) {
  return '<form class="well answer-form"><div class="loading"></div><div class="form-inline"><div class="input-group"><span class="input-group-addon"><span class="glyphicon glyphicon-film"></span></span><input class="autocomplete input-lg form-control" size="16" type="text" autocomplete="off"></div><a href="#" class="btn btn-lg btn-success" id="btn-search">Search</a><a href="#" class="btn btn-lg btn-warning" id="btn-clear">Clear</a></div><div class="controls rows"><div class="suggestions"><p class="suggest-info">Search for a film, select your answer then submit.</p></div></div><div class="guess-buttons"><a href="#" class="btn btn-primary" id="btn-submit">Submit</a><a href="#" class="btn btn-danger pull-left" id="btn-pass">No idea, another clue please</a></div></form>';
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.option = function(opt_data, opt_ignored) {
  return '<label class="radio' + ((opt_data.odd) ? ' odd' : '') + '"><input type="radio" name="' + soy.$$escapeHtml(opt_data.fieldName) + '" value="' + soy.$$escapeHtml(opt_data.key) + '">' + soy.$$escapeHtml(opt_data.title) + '<span>' + soy.$$escapeHtml(opt_data.year) + '</span></label>';
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.guess = function(opt_data, opt_ignored) {
  opt_data = opt_data || {};
  return '<div class="alert alert-warning failed-guess">' + ((opt_data.title) ? '<b>' + soy.$$escapeHtml(opt_data.title) + ' (' + soy.$$escapeHtml(opt_data.year) + ')</b> is incorrect. Try again!' : '<b>PASS</b>') + '</div>';
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.clue = function(opt_data, opt_ignored) {
  return '<div class="' + ((opt_data.image) ? 'thumbnail' : 'alert alert-info clue') + '">' + ((opt_data.image) ? '<img src="' + soy.$$escapeHtml(opt_data.image) + '" width="910" height="343">' + ((opt_data.position) ? '<div class="caption">' + ((opt_data.position) ? '<h4>Clue #' + soy.$$escapeHtml(opt_data.position) + '</h4>' : '') + ((opt_data.text) ? '<p>' + soy.$$escapeHtml(opt_data.text) + '</p>' : '') + '</div>' : '') : (opt_data.text) ? '<p><b>Clue #' + soy.$$escapeHtml(opt_data.position) + ': </b>' + soy.$$escapeHtml(opt_data.text) + '</p>' : '') + '</div>';
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.answer = function(opt_data, opt_ignored) {
  return '<div class="alert clearfix alert-' + ((opt_data.correct) ? 'success' : 'danger') + ' clue"><h4 class="alert-heading">' + ((opt_data.correct) ? (opt_data.numGuesses == 1) ? 'BOOM!' : (opt_data.numGuesses == 2) ? 'Well played!' : (opt_data.numGuesses == 3) ? 'Correct!' : 'That’s the one!' : 'Incorrect!') + '</h4><img src="' + soy.$$escapeHtml(opt_data.packshot) + '" class="pull-left packshot thumbnail"><p>The answer is of course: <b>' + soy.$$escapeHtml(opt_data.title) + '</b> (' + soy.$$escapeHtml(opt_data.year) + ')</p><p>You used <b>' + soy.$$escapeHtml(opt_data.numGuesses - 1) + '</b> clues and scored <b>' + soy.$$escapeHtml(opt_data.score) + '</b> points</p><p>Your average score is now <b>' + soy.$$escapeHtml(opt_data.averageScore) + '</b> and your average clues used is <b>' + soy.$$escapeHtml(opt_data.averageClues) + '</b></p><p>Check out how this all looks on the <a href="/leaderboard">Leaderboard</a></p><p>And here\'s the film on <a href="' + soy.$$escapeHtml(opt_data.imdb_url) + '">IMDB</a></p><p><b><i>Thanks for playing, and see you next week!</i><br>FMJ</b></p></div>';
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.score = function(opt_data, opt_ignored) {
  var output = '<div><h4>Points available:</h4><p class="points-available">';
  var sList139 = opt_data.score;
  var sListLen139 = sList139.length;
  for (var sIndex139 = 0; sIndex139 < sListLen139; sIndex139++) {
    var sData139 = sList139[sIndex139];
    output += '<span class="point">' + soy.$$escapeHtml(sData139) + '</span>';
  }
  output += '<sub></sub></p><h4>Clues:</h4><div class="progress"><div class="bar' + ((opt_data.clueCount > 1) ? ' bar-active' : '') + ' bar-1">1</div><div class="bar' + ((opt_data.clueCount > 2) ? ' bar-active' : '') + ' bar-2">2</div><div class="bar' + ((opt_data.clueCount > 3) ? ' bar-active' : '') + ' bar-3">3</div></div></div>';
  return output;
};


/**
 * @param {Object.<string, *>=} opt_data
 * @param {(null|undefined)=} opt_ignored
 * @return {string}
 * @notypecheck
 */
ffc.template.quiz.realtimeScore = function(opt_data, opt_ignored) {
  return '<div><a href="/u/' + soy.$$escapeHtml(opt_data.user) + '"><img src="' + soy.$$escapeHtml(opt_data.pic) + '" width="20" height="20">&nbsp;' + soy.$$escapeHtml(opt_data.user) + '&nbsp;</a>(' + soy.$$escapeHtml(opt_data.score) + ')</div>';
};
