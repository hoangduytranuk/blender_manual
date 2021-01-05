#!/bin/bash
cd $BLENDER_MAN_EN/build/gettext
out_file=~/temp.txt
temp_file=~/tmp.txt
echo "" > $out_file
echo "" > $temp_file
for f in $(find . -name '*.pot'): 
do
    # echo $f
    # echo "------" $out_file    
    # grep -o -E "[^\w]'[^']+'" $f # single quote
    egrep -o '(msgid "[^"]).*"' $f | sed 's/msgid "//g' | sed 's/"$//g' > $out_file
    # # arched bracket
    # cat $out_file | grep -o -E '\([^\(\)]+\)' | grep -o -E '\([^\(\)]+\)' | sed 's/(//g' | sed 's/)//g' 
    ## arched bracket original form
    # cat $out_file | grep -o -E '(^|\s)\([^\(\)]+\)'
    # cat $out_file | grep -o -E '(^|\s)\([^\(\)]+\)'
    cat $out_file | grep -o -E 'stand \w+ \w+' >> $temp_file
    ## function declaration forms, ie. func(a, b, c)
    # cat $out_file | grep -o -E '\w+\([^\(\)]+\)' 
    # # double quote
    # cat $out_file | grep -o -E '"[^"]+"' | sed 's/\\//g' | sed 's/"//g' 
    # # # single quote    
    # cat $out_file | grep -o -E "'[^']+'" | sed "s/^'//g" | sed "s/'$//g"
    # cat $out_file | grep -o -E "(:\w+:)?[\`]+[^\`]+[\`]+"
    # cat $out_file | grep -E "\w+:\w+" > $temp_file
    # if [ -s $temp_file ]; then
    #     echo "$f";
    #     echo "------------- >>";
    #     cat $out_file | grep -o -E "\w+:\w+"
    #     cat $temp_file;
    #     echo "------------- <<";
    # fi
    # if [ ! -z $result ]; then
    #     echo "FOUND: $f"
    #     cat $out_file | grep -o -E "\w+:\w+"
    # fi
    # # asterisk quote
    # cat $out_file | grep -o -E "\*[^\*]+\*" | sed 's/*//g' 
    # :kbd:
    # cat $out_file | grep -o -E ':\w+:\`([^\`]+)' | grep -o -E '\`([^\`]+)\`' | sed 's/\`//g' | sed 's/<[^<>]\+>//g' 
    # grep -o -E "[^\\]\"[^\"]+\"" $f # double quote
    # grep -o -E "[^a-zA-Z0-9]'[^']+'" $f >> $out_file
    # #    grep -o -E ':[[:alnum:]]+:\`([^\`]+)' $f | grep -o -E '\`([^\`]+)\`' | sed 's/\`//g' | sed 's/<[^<>]\+>//g' >> $out_file
#     grep -o -E ':[[:alnum:]]+:\`([^\`]+)' $f | sed 's/\<[^<>]+\>//g'
done
# done > ~/findgettext.log
cat $temp_file | sort | uniq -c | sort > $out_file

# f=./editors/image/introduction.pot
# grep -o -E ':[[:alnum:]]+:\`([^\`]+)\`' $f 
# grep -o -E ':[[:alnum:]]+:\`([^\`]+)\`' $f | sed 's/:[^:]*://g' | sed 's/\`//g' | sed 's/\<.*\>//g' 
