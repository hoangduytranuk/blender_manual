#!/bin/bash
store_file=~/Documents/changes_temp.txt;
echo "" > $store_file;
file_list=$(find $BLENDER_MAN_VI -name "*.po" -print|sort);
for f in $file_list; do
    grep_list=$(grep -E "msgstr \"([ ]?)(-- )" $f);
    if [[ ! -z "$grep_list" ]]; then
        echo $f >> $store_file;
        printf %100s | tr " " "=" >> $store_file;
        echo "" >> $store_file;
        grep -E "msgstr \"([ ]?)(-- )" $f >> $store_file;
    fi
done
kwrite $store_file &
