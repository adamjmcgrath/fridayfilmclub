#!/bin/bash
#
# Copyright 2011 Friday Film Club Inc.  All Rights Reserved.
#
# Tools for compiling JavaScript using the Closure Compilers.

CLOSURE_LIB=./src/closure-library
CLOSURE_TEMPLATES=./src/closure-templates/javascript
CLOSURE_SRC=$CLOSURE_LIB/closure
CLOSURE_BUILDER_PATH=$CLOSURE_LIB/closure/bin/build/closurebuilder.py
CLOSURE_DEPSWRITER_PATH=$CLOSURE_LIB/closure/bin/build/depswriter.py
CLOSURE_COMPILER_PATH=$CLOSURE_JAR
CLOSURE_TEMPLATES_COMPILER_PATH=$SOY_JAR

FFC_PATH=./src
FFC_SOURCE=$FFC_PATH/javascript
API_SOURCE=$FFC_SOURCE/api
QUIZ_SOURCE=$FFC_SOURCE/quiz
LEAGUE_SOURCE=$FFC_SOURCE/league
USER_SUGGEST_SOURCE=$FFC_SOURCE/usersuggest
LEADERBOARD_SOURCE=$FFC_SOURCE/leaderboard
SUGGEST_SOURCE=$FFC_SOURCE/suggest
TEMPLATE_SOURCE=$FFC_SOURCE/template
GROW_SOURCE=$FFC_PATH/growjs
FFC_QUIZ_JS_OUTPUT=$FFC_PATH/static/js/quiz.js
FFC_LEADERBOARD_JS_OUTPUT=$FFC_PATH/static/js/leaderboard.js
FFC_SETTINGS_JS_OUTPUT=$FFC_PATH/static/js/settings.js
FFC_LEAGUE_FORM_JS_OUTPUT=$FFC_PATH/static/js/leagueform.js
FFC_DEPS_OUTPUT=$FFC_PATH/static/js/deps.js
EXTERNS_SOURCE=$FFC_SOURCE/externs


if [ $1 == "deps" ] || [ $1 == "all" ]; then
  echo 'Building deps'
  python $CLOSURE_DEPSWRITER_PATH \
    --root_with_prefix="$FFC_SOURCE ../../../javascript/"\
    --root_with_prefix="$CLOSURE_TEMPLATES ../../../closure-templates/javascript/"\
    --root_with_prefix="$GROW_SOURCE ../../../growjs/"\
    > $FFC_DEPS_OUTPUT
  echo 'Written deps to '$FFC_DEPS_OUTPUT
fi

if [ $1 == "template" ] || [ $1 == "all" ]; then
  echo 'Building template'
  java -jar $CLOSURE_TEMPLATES_COMPILER_PATH \
    --shouldProvideRequireSoyNamespaces \
    --shouldGenerateJsdoc \
    --outputPathFormat src/javascript/template/{INPUT_FILE_NAME_NO_EXT}.soy.js \
    src/templates/soy/*.soy
fi

if [ $1 == "quiz" ] || [ $1 == "all" ]; then
  echo 'Building quiz'
  python $CLOSURE_BUILDER_PATH \
    --root=$CLOSURE_LIB \
    --root=$CLOSURE_TEMPLATES \
    --root=$API_SOURCE \
    --root=$QUIZ_SOURCE \
    --root=$SUGGEST_SOURCE \
    --root=$TEMPLATE_SOURCE \
    --root=$GROW_SOURCE \
    --namespace="ffc.quiz.Question" \
    --namespace="ffc.quiz.RealtimeScores" \
    --output_mode=compiled \
    --compiler_jar=$CLOSURE_COMPILER_PATH \
    --compiler_flags="--compilation_level=ADVANCED_OPTIMIZATIONS" \
    --compiler_flags="--externs=$EXTERNS_SOURCE/channel.js" \
    --compiler_flags="--output_wrapper=\"(function() {%output%})();\"" \
    > $FFC_QUIZ_JS_OUTPUT
fi

if [ $1 == "leaderboard" ] || [ $1 == "all" ]; then
  echo 'Building leaderboard'
  python $CLOSURE_BUILDER_PATH \
    --root=$CLOSURE_LIB \
    --root=$CLOSURE_TEMPLATES \
    --root=$API_SOURCE \
    --root=$LEADERBOARD_SOURCE \
    --root=$TEMPLATE_SOURCE \
    --root=$GROW_SOURCE \
    --namespace="ffc.leaderboard.LeaderBoardToggler" \
    --namespace="ffc.leaderboard.LeaderBoard" \
    --output_mode=compiled \
    --compiler_jar=$CLOSURE_COMPILER_PATH \
    --compiler_flags="--compilation_level=ADVANCED_OPTIMIZATIONS" \
    --compiler_flags="--externs=$EXTERNS_SOURCE/channel.js" \
    --compiler_flags="--output_wrapper=\"(function() {%output%})();\"" \
    > $FFC_LEADERBOARD_JS_OUTPUT
fi

if [ $1 == "settings" ] || [ $1 == "all" ]; then
  echo 'Building settings'
  python $CLOSURE_BUILDER_PATH \
    --root=$CLOSURE_LIB \
    --root=$CLOSURE_TEMPLATES \
    --root=$API_SOURCE \
    --root=$SUGGEST_SOURCE \
    --root=$TEMPLATE_SOURCE \
    --namespace="ffc.suggest.AutoComplete" \
    --output_mode=compiled \
    --compiler_jar=$CLOSURE_COMPILER_PATH \
    --compiler_flags="--compilation_level=ADVANCED_OPTIMIZATIONS" \
    --compiler_flags="--output_wrapper=\"(function() {%output%})();\"" \
    > $FFC_SETTINGS_JS_OUTPUT
fi

if [ $1 == "leagueform" ] || [ $1 == "all" ]; then
  echo 'Building settings'
  python $CLOSURE_BUILDER_PATH \
    --root=$CLOSURE_LIB \
    --root=$CLOSURE_TEMPLATES \
    --root=$API_SOURCE \
    --root=$USER_SUGGEST_SOURCE \
    --root=$LEAGUE_SOURCE \
    --root=$TEMPLATE_SOURCE \
    --namespace="ffc.usersuggest.AutoComplete" \
    --namespace="ffc.league.UsersModel" \
    --namespace="ffc.league.Form" \
    --output_mode=compiled \
    --compiler_jar=$CLOSURE_COMPILER_PATH \
    --compiler_flags="--compilation_level=ADVANCED_OPTIMIZATIONS" \
    --compiler_flags="--output_wrapper=\"(function() {%output%})();\"" \
    > $FFC_LEAGUE_FORM_JS_OUTPUT
fi
