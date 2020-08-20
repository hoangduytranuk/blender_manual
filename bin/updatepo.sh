#!/bin/zsh -x
cd $BLENDER_MAN_EN
sphinx-build -t builder_html -b gettext  -j "8" manual build/locale
pot_file_list = $(find build/locale -name "*.pot")

