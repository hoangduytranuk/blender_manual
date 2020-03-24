#!/bin/bash
cd $BLENDER_MAN_EN_DEV
# git commit -am "$1"
# git push
# cd $BLENDER_MAN_EN
# git checkout master
# git pull https://hoangduytranuk@github.com/hoangduytranuk/blender_manual.git development
# git push
git commit -am "$1"
git rebase origin/master
git checkout master
git merge development
git push
git checkout development
git push
