#!/bin/bash
#
# Copyright 2011 Friday Film Club Inc.  All Rights Reserved.
#
# Tools for compiling JavaScript using the Closure Compilers.

CLOSURE_LIB=./src/closure-library
CLOSURE_SRC=$CLOSURE_LIB/closure
CLOSURE_BUILDER_PATH=$CLOSURE_LIB/closure/bin/build/closurebuilder.py
CLOSURE_DEPSWRITER_PATH=$CLOSURE_LIB/closure/bin/build/depswriter.py
CLOSURE_COMPILER_PATH=/Users/amcgrath/bin/compiler.jar

FFC_PATH=./src
FFC_SOURCE=$FFC_PATH/javascript
FFC_JS_OUTPUT=$FFC_PATH/static/js/quiz.js
FFC_DEPS_OUTPUT=$FFC_PATH/static/js/deps.js

MODE=$1

if [ $1 == "deps" ]; then
  $CLOSURE_DEPSWRITER_PATH \
    --root_with_prefix="$FFC_SOURCE ../../../javascript/"\
    > $FFC_DEPS_OUTPUT
  echo 'Written deps to '$FFC_DEPS_OUTPUT
fi

if [ $1 == "build" ]; then
  $CLOSURE_BUILDER_PATH \
    --root=$CLOSURE_LIB \
    --root=$FFC_SOURCE \
    --namespace="ffc.Question" \
    --output_mode=compiled \
    --compiler_jar=$CLOSURE_COMPILER_PATH \
    --compiler_flags="--compilation_level=ADVANCED_OPTIMIZATIONS" \
    > $FFC_JS_OUTPUT
fi
