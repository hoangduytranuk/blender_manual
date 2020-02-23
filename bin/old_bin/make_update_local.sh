#!/bin/bash -x
cd $BLENDER_MAN_EN
#make clean
#make gettext
sphinx-intl update -p build/locale -l "vi"
