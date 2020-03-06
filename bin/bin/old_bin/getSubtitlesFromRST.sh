#!/bin/bash
po_dir="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"
root_dir="/home/htran/blender_documentations/blender_docs/build/rstdoc"
temp_file="/home/htran/rstdoc_temp.txt"
temp_file_0001="/home/htran/rstdoc_temp_0001.txt"
temp_file_0002="/home/htran/rstdoc_temp_0002.txt"
final_file="/home/htran/rstdoc_final_0004_0001.txt"
file_list=$(find $root_dir -name "*.rst")

declare -a word_list=()

getWordList()
{
    echo "" > $final_file
    declare -a kw=("title" "field_name" "term" "strong" "rubric")
    for f in $file_list;
    do
        echo "" > $temp_file
        echo "" > $temp_file_0001
        echo "" > $temp_file_0002
        for k in ${kw[@]};
        do
            p_0001=$(printf "<%s[^>]*>(.*?)</%s>" $k $k)
            p_0002=$(printf "<%s[^>]*>(.*?)<" $k)
            p_0003="(term ids)*(>)(.*?)"
            sed_01_start=$(printf "s|<%s>||g" $k)
            sed_01_end_01=$(printf "s|<\/%s>||g" $k)
            sed_01_end_02="s|<||g"
            sed_02="s|(term ids.*>)||g"
            sed_break_down_0001="s|> <|>\n<|g"
            sed_break_down_0002="s|><|>\n<|g"

            #title_1=$(cat $f | grep -Eo $p_0001 | sed "$sed_break_down_0001" | sed "$sed_break_down_0002" )
            title_2=$(cat $f | grep -Eo $p_0002 | sed "$sed_break_down_0001" | sed "$sed_break_down_0002" )

            found_debug=0
#             if [ ! -z "$title_1" ]; then
# #                 found_line=$(echo $title_1 | sed "$sed_break_down_0001" | sed "$sed_break_down_0002"  | sed "$sed_01_start" | sed "$sed_01_end_01" | sed -E "$sed_02")
#                 #echo $title_1 | sed 's|> <|>\n<|g' | sed 's|><|>\n<|g' | tee $temp_file
#                 #echo $title_1 | sed "$sed_break_down_0001" | sed "$sed_break_down_0002" | tee $temp_file
#                 #found_debug=$(echo $title_1 | grep -c "Disable Collisions")
#                 echo $title_1 | grep -Eo $p_0001 | sed "$sed_break_down_0001" | sed "$sed_break_down_0002" | grep -Eo $p_0001
#                 echo $title_1 | grep -Eo $p_0001 | sed "$sed_break_down_0001" | sed "$sed_break_down_0002" | grep -Eo $p_0001 | sed "$sed_01_start" | sed "$sed_01_end_01"  >> $temp_file_0001
#                 #echo $title_1 | sed "$sed_break_down_0001" | sed "$sed_break_down_0002" | grep --color=always -Eo $p_0001 | sed "$sed_01_start" | sed "$sed_01_end_01" | sed -E "$sed_02" | tee $temp_file
#             fi
            if [ ! -z "$title_2" ]; then
                echo $title_2 | grep -Eo $p_0002 | sed "$sed_break_down_0001" | sed "$sed_break_down_0002" | grep -Eo $p_0002
                echo $title_2 | grep -Eo $p_0002 | sed "$sed_break_down_0001" | sed "$sed_break_down_0002" | grep -Eo $p_0002 | sed "$sed_01_start" | sed "$sed_01_end_01" >> $temp_file
#                 found_line=$(echo $title_2 | sed 's|> <|>\n<|g' | sed 's|< <|\n<|g' | sed $sed_01_start | sed $sed_01_end_02 | sed -E 's|(term ids.*>)||g')
#                 echo $found_line | tee $temp_file
            fi
            #filteringDuplicationFromTempFiles

#             if [ $found_debug -gt 0 ]; then
#                 #echo $title_1 | grep --color=always -Eo $p_0001 | sed "$sed_break_down_0001" | sed "$sed_break_down_0002" | grep --color=always -Eo $p_0001
#                 echo "------------------------" | tee $final_file
#                 echo "File: $f" | tee $final_file
#                 exit
#             fi
        done
        if [ ! -z $temp_file ]; then
            echo "------------------------"
            echo "File: $f"
            echo "------------------------"
            cat $temp_file | sort -u
            cat $temp_file | sort -u >> $final_file
        fi
    done
    cat $final_file | sort -u
    cat $final_file | sort -u > $temp_file
    mv $temp_file $final_file
}


filteringDuplicationFromTempFiles()
{
    echo $temp_file_0001
    cat $temp_file_0001
    echo "--------"
    echo $temp_file_0002
    cat $temp_file_0002
    echo "--------"
    while read -r line;
    do
        match=$(grep -c "$test_line.*" $temp_file_0002);
        [ $match -gt 0 ] && echo "found repeat:[$line]";
        [ $match -gt 0 ] && grep -v $test_line $temp_file_0002 >> $temp_file;
        [ $match -gt 0 ] && grep -v $test_line $temp_file_0001 >> $temp_file;
    done < $temp_file_0001
    echo "Sorting:[$temp_file]";
    cat $temp_file | sort -u | tee $final_file
    #cat $temp_file | sort -u >> $final_file
    #mv $temp_file $final_file
}


checkFinal()
{
    check_file="/home/htran/rstdoc_final_0004.txt"
    input_file="/home/htran/rstdoc_final_0004_0001.txt"
    echo "" > $temp_file
    exclude_file="$1";
    while read -r line;
    do
        match=$(grep -c "$line" $check_file);
        [ $match -eq 0 ] && echo $line;
        [ $match -gt 0 ] && echo $line >> $temp_file;
    done < $input_file
    cat $temp_file | sort -u >> $final_file
    #mv $temp_file $final_file
}

#checkFinal

printArray(){
    array=$1
    for a in ${array[@]}; do
        echo $a
    done
}

validateEntries()
{
    rst_lines=();
    rst_pattern=()
    while read -r check_line;
    do
        rst_lines+=($check_line)
        rst_pattern+=("msgid \\\"$check_line\\\"")
    done < $1
#     for a in "${rst_pattern[@]}"; do
#         item=$(printf "%s\n" $a);
#         echo $item
#     done
#     exit
    po_list=$(find $po_dir -name "*.po")
    for po_file in $po_list;
    do
        echo "checking $po_file"
        echo "---------------------"
        for pattern in "${rst_pattern[@]}"; do
            echo $pattern
            match_count=$(grep -c "$pattern" $po_file)
            [ $match_count -gt 0 ] && echo $pattern;
        done
        #[ $match -eq 0 ] && echo $pattern;
        #[ $match_count -gt 0 ] && echo $line >> $temp_file;
    done
    cat $temp_file
}

filterWordList()
{
    echo "" > $temp_file
    echo "" > $output_file
    exclude_file="$1";
    while read -r line;
    do
        test_line=$(echo $line | sed -E 's/[^[:alnum:][:space:]]+/\\&/g')
        echo "[$test_line]"
        match=$(grep -Ec "$test_line" $exclude_file);
        [ ! $match -gt 0 ] && echo $line >> $temp_file;
    done < $input_file
    cat $temp_file | sort -u >> $output_file
    #mv $output_file $input_file
}

local_exclude_file="/home/htran/rst_exclude.txt";
current_dic="/home/htran/menuselection_new_dictionary_sorted_translated_0027.json"
input_file="/home/htran/rstdoc_final_0004_0001.txt"
output_file="/home/htran/rstdoc_final_0004_0002.txt"
getWordList
#validateEntries $final_file
#getWordList

#filterWordList $local_exclude_file
#filterWordList $current_dic

