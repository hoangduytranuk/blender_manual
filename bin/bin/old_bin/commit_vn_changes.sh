#!/bin/bash -x
DIFF=$HOME/Documents/patch.diff
COMMENT="$1"
cd $BLENDER_MAN_VI
change_placeholders.py -d $PWD -t 1d
svn diff > $DIFF
svn commit -m "$COMMENT"
svn update .
cd $BLENDER_MAN_VI_DEV
patch -p0 < $DIFF
change_placeholders.py -d $PWD -t 1d
git commit -am "$COMMENT"
git push
