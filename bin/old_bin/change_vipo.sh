#!/bin/bash
cd $BLENDER_MAN_EN

#for lang in `find locale/ -maxdepth 1 -mindepth 1 -type d -not -iwholename '*.svn*' -printf '%f\n' | sort`; do
sphinx-intl change -p build/locale -l "vi"
#done
