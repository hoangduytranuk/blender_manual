#!/bin/bash
list_file=$(find $BLENDER_MAN_EN/build/rstdoc -name "*.rst" | sort);
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
    grep -En -B 2 -A 2  "$1" $file
    echo $file
    echo "-----------------"
done
