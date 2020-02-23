#!/bin/bash
list_file=$(find $BLENDER_MAN_EN/manual/ -name "*.rst" | sort);
#list_file=$(find $BLENDER_MAN_EN/build/rstdoc -name "*.html" | sort);
#echo $list_file
outfile=~/find_manual.txt
for file in $list_file;
do
    #is_in_file=$(cat $file | grep -Ec ":menuselection:\`[^\`\(\)].*\`" | grep -Evc "[\(\)]" | grep -Evc "msgstr");
    is_in_file=$(cat $file | grep -Eoc "$1");
    [ $is_in_file -ne 0 ] && echo $file
done > $outfile
#cat $outfile
for file in $(cat $outfile);
do
	if [ -z $2 ]; then
		grep -En -B 2 -A 2  "$1" $file
	else
		grep --color=always -En -B 2 -A 2  "$1" $file
	fi
    echo $file
    echo "-----------------"
done
