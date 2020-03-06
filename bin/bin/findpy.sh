#!/bin/bash
LOCAL_LIB_DIR=$LOCAL_PYTHON_3
list_file=$(find $LOCAL_LIB_DIR -name "*.py" | sort);
outfile=~/find_py.txt
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
