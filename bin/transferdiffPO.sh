#!/bin/bash
md5exec=/usr/bin/md5sum
left_dir=$1
right_dir=$2
list_left=$(find $left_dir -type f -name "*.po" | sort)
list_right=$(find $right_dir -type f -name "*.po" | sort)

cut_len=`expr ${#left_dir}+1`
for left_file_name in $list_left; do
    common_name=${left_file_name:${cut_len}}
    right_file_name=$right_dir$common_name
    test_fine=$(echo $list_right | grep "$common_name")
    if [  -e $right_file_name ]; then
        #echo "You're there $right_file_name"
        content_of_left=$(sed '1,/^$/d' $left_file_name)
        content_of_right=$(sed '1,/^$/d' $right_file_name)
        #echo $content_of_left
        md5sum_left=$(echo $content_of_left | $md5exec)
        md5sum_right=$(echo $content_of_right | $md5exec)
        #echo "md5sum_left: $md5sum_left; md5sum_right: $md5sum_right"
        if [ "$md5sum_left" != "$md5sum_right" ]; then
            $HOME/bin/transferPO.py -f $left_file_name -o $right_file_name
            exit
        fi
    else
        echo "NOT FOUND: $right_file_name"
    fi
done
