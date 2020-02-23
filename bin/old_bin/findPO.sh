#!/bin/bash
is_color=$2
list_file=$(find $BLENDER_MAN_EN/locale/vi/LC_MESSAGES -name "*.po" | sort);
outfile=~/find_po.txt
for file in $list_file;
do
    #is_in_file=$(cat $file | grep -Ec ":menuselection:\`[^\`\(\)].*\`" | grep -Evc "[\(\)]" | grep -Evc "msgstr");
    is_in_file=$(cat $file | grep -Ec "$1");
    [ $is_in_file -ne 0 ] && echo $file
done > $outfile
#cat $outfile
for file in $(cat $outfile);
do
    if [ ! -z $is_color ]; then
        grep --color=always -En "$1" $file
        #grep --color=always -En -o -B 2 -A 2  "$1" $file
        #grep --color=always -En -o "$1" $file
    else
        grep -En "$1" $file
        #grep -En -o -B 2 -A 2  "$1" $file
        #grep -En -o o"$1" $file
    fi
    echo $file
    echo "-----------------"
done
