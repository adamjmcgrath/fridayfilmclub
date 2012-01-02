#!/bin/bash
#
# Copyright 2011 Friday Film Club Inc.  All Rights Reserved.
#
# Tools for compiling JavaScript using the Closure Compilers.

CLOSURE_LIB=./closure-library
CLOSURE_SRC=$CLOSURE_LIB/closure
CLOSURE_BUILDER_PATH=$CLOSURE_LIB/closure/bin/build/closurebuilder.py
CLOSURE_DEPSWRITER_PATH=$CLOSURE_LIB/closure/bin/build/depswriter.py
CLOSURE_COMPILER_PATH=/Users/amcgrath/bin/compiler.jar

FFC_PATH=.
FFC_SOURCE=$FFC_PATH/javascript
FFC_JS_OUTPUT=$FFC_PATH/static/js/quiz.js
FFC_DEPS_OUTPUT=$FFC_PATH/static/js/deps.js

MODE=$1

if [ !$1 ]; then
  echo "foo"
fi

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
    --namespace="ffc.AutoComplete" \
    --output_mode=compiled \
    --compiler_jar=$CLOSURE_COMPILER_PATH \
    --compiler_flags="--compilation_level=ADVANCED_OPTIMIZATIONS" \
    > $FFC_JS_OUTPUT
fi

# 
# 
# 
# # /Users/amcgrath/Documents/code/closure/closure/bin/calcdeps.py \
# #   -i /Users/amcgrath/Sites/fridayfilmclub/javascript/autocomplete.js \
# #   -p /Users/amcgrath/Documents/code/closure \
# #   -p /Users/amcgrath/Sites/fridayfilmclub/javascript \
# #   -f "--formatting=pretty_print" \
# #   -o compiled \
# #   -c /Users/amcgrath/bin/compiler.jar \
# #   > /Users/amcgrath/Sites/fridayfilmclub/static/js/quiz.js
# 
# # /Users/amcgrath/Documents/code/closure/closure/bin/calcdeps.py \
# #   -i /Users/amcgrath/Sites/fridayfilmclub/javascript/autocomplete.js \
# #   -p /Users/amcgrath/Documents/code/closure \
# #   -p /Users/amcgrath/Sites/fridayfilmclub/javascript \
# #   -f "--formatting=pretty_print" \
# #   -o deps \
# #   -c /Users/amcgrath/bin/compiler.jar \
# #   > /Users/amcgrath/Sites/fridayfilmclub/javascript/deps.js
# 
# 
# /Users/amcgrath/Documents/code/closure/closure/bin/build/closurebuilder.py \
#   --root=/Users/amcgrath/Documents/code/closure/ \
#   --root=/Users/amcgrath/Sites/fridayfilmclub/javascript/ \
#   --namespace="ffc.AutoComplete" \
#   --output_mode=compiled \
#   --compiler_jar=/Users/amcgrath/bin/compiler.jar \
#   --compiler_flags="--formatting=pretty_print" \
#   > /Users/amcgrath/Sites/fridayfilmclub/static/js/quiz.js