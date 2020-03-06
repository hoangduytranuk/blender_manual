#!/bin/bash
#/home/htran/blender_documentations/blender_docs/build/rstdoc/animation/motion_paths.html

html_file=$1

po_file=$(echo $html_file | sed 's|build\/rstdoc|locale/vi/LC_MESSAGES|g' | sed 's|\.html|\.po|g')
cmd="kwrite $po_file"
echo $cmd

beauty_file=$(echo $html_file | sed 's|rstdoc|rstdoc_beauty|g')
cmd="kwrite $beauty_file"
kwrite $beauty_file $po_file &

