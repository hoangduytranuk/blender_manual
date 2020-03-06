#!/bin/bash
list_file=$(find $BLENDER_MAN_EN/locale/vi/LC_MESSAGES -name "*.po" | sort);
outfile=/home/htran/temp.txt

printSepLine(){
    char=$1
    yes $char | head -10 | paste -s -d '' -
}

processOutFile(){
    f=$1
    printSepLine "-"
    echo $f
    printSepLine "-"
    while read -r line; do
        python3 -c "import re; word_list=re.search(r\":menuselection:\`(.*\)\`\", $line); print(word_list)"
        exit 0
    done < $outfile
    printSepLine "-"
}

for file in $list_file;
do
    grep -E ":menuselection:\`[^\`\(\)].*\`" $file | grep -Ev "[\(\)]" | grep -Ev "msgid" > $outfile

    [ -s $outfile ] && processOutFile $file

    #echo $find_result
#     if [ "$find_result" -ne "" ] ;
#     then
#         echo $file
#         echo "=========================="
#     fi
done

