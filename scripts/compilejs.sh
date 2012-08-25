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
CLOSURE_COMPILER_PATH=~/bin/compiler.jar
CLOSURE_TEMPLATES_COMPILER_PATH=~/bin/SoyToJsSrcCompiler.jar

FFC_PATH=./src
FFC_SOURCE=$FFC_PATH/javascript
QUIZ_SOURCE=$FFC_SOURCE/quiz
SUGGEST_SOURCE=$FFC_SOURCE/suggest
TEMPLATE_SOURCE=$FFC_SOURCE/template
FFC_JS_OUTPUT=$FFC_PATH/static/js/quiz.js
FFC_DEPS_OUTPUT=$FFC_PATH/static/js/deps.js


if [ $1 == "deps" ]; then
  $CLOSURE_DEPSWRITER_PATH \
    --root_with_prefix="$FFC_SOURCE ../../../javascript/"\
    --root_with_prefix="$CLOSURE_TEMPLATES ../../../closure-templates/javascript/"\
    > $FFC_DEPS_OUTPUT
  echo 'Written deps to '$FFC_DEPS_OUTPUT
fi


if [ $1 == "build" ]; then
  $CLOSURE_BUILDER_PATH \
    --root=$CLOSURE_LIB \
    --root=$CLOSURE_TEMPLATES \
    --root=$QUIZ_SOURCE \
    --root=$SUGGEST_SOURCE \
    --root=$TEMPLATE_SOURCE \
    --namespace="ffc.quiz.Question" \
    --output_mode=compiled \
    --compiler_jar=$CLOSURE_COMPILER_PATH \
    --compiler_flags="--compilation_level=ADVANCED_OPTIMIZATIONS" \
    --compiler_flags="--output_wrapper=\"(function() {%output%})();\"" \
    > $FFC_JS_OUTPUT
fi

if [ $1 == "template" ]; then
  java -jar $CLOSURE_TEMPLATES_COMPILER_PATH \
    --shouldProvideRequireSoyNamespaces \
    --shouldGenerateJsdoc \
    --outputPathFormat src/javascript/template/{INPUT_FILE_NAME_NO_EXT}.soy.js \
    src/templates/soy/*.soy
fi
