#!/bin/bash
is_color=$2
list_file=$(find $BLENDER_GIT -type f  ! -path "*/locale/*" | sort);
outfile=~/find_code.txt
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
        grep --color=always -En -B 2 -A 2  "$1" $file
    else
        grep -En -B 2 -A 2  "$1" $file
    fi
    echo $file
    echo "-----------------"
done
