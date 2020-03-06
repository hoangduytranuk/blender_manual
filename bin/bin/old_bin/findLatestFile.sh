#!/bin/bash
YOUR_NAME="Hoang Duy Tran"
YOUR_EMAIL="hoangduytran1960@googlemail.com"
YOUR_ID="$YOUR_NAME <$YOUR_EMAIL>"
YOUR_TRANSLATION_TEAM="London, UK <$YOUR_EMAIL>"
#YOUR_TRANSLATION_TEAM_EMAIL="$YOUR_EMAIL"
YOUR_LANGUAGE_CODE="vi"

date_bin=/usr/bin/date
time_now=$($date_bin +"%F %H:%M%z")
declare -A pattern_list=(
["FIRST AUTHOR.*SS>"]="$YOUR_ID"
["Last-Translator.*>"]="Last-Translator: $YOUR_ID"
["PO-Revision-Date: [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\+[0-9]{4}"]="PO-Revision-Date: ${time_now}"
["PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE"]="PO-Revision-Date: ${time_now}"
["Language-Team:.*>"]="Language-Team: $YOUR_TRANSLATION_TEAM"
)

re_language_code="Language:.*vi"
language_code="\"Language: vi\\\\n\"\n"
declare -A pattern_insert=(
["\"MIME-Version"]="$language_code\"MIME-Version"
)

function findChangedFiles()
{
    #latest_file=$(find . -type f -name "*.po" -newermt $(date +%F) -ls | sort | tail -n 1 | awk '{ print $11 }')
    if [ -d ".git" ]; then
        changed_list=$(git status | grep 'modified' | awk '{ print $2 }' | grep ".po")
    elif [ -d ".svn" ]; then
        changed_list=$(svn status | grep 'M' | awk '{ print $2 }'| grep ".po")
    else
        changed_list=""
    fi
    #latest_file=$(find . -type f -name "*.po" -exec ls -al --time-style=+%D\ %H:%M:%S {} \; | grep `/usr/bin/date +%D` | awk '{ print $6,$7,$8 }' | sort | tail -1 | awk '{ print $3 }')
}

function replaceAllChangedFiles()
{
    findChangedFiles
    for f in $changed_list; do
        listFileContent "$f"
    done
}

function replaceRegularStrings()
{
    changed_file=$1
    #test_file="$HOME/testfile.po"
    for i in "${!pattern_list[@]}"; do
        #printf "%s\t%s\n" "$i" "${pattern_list[$i]}"
        pattern="$i"
        value="${pattern_list[$i]}"
        echo "$pattern => $value"
        #cat $changed_file | sed 's|${pattern}|${value}|g'
        sed -i "s|${pattern}|${value}|g" $changed_file
    done
}

function insertLanguageCode()
{
    changed_file=$1
    current_line=$(grep $re_language_code $changed_file)
    #echo "current_line=[$current_line]"
    if [ "$current_line" != "" ]; then
        echo "has Language code"
    else
        for i in "${!pattern_insert[@]}"; do
            pattern="$i"
            value="${pattern_insert[$i]}"
            echo "Replacing: $pattern => $value"
            sed -i "s|${pattern}|${value}|g" $changed_file
        done
    fi
}

function listFileContent()
{
    changed_file=$1
    #cat $changed_file
    echo "$changed_file"
}

cwd=$1
if [[ ! -z  "$cwd" ]]; then
    echo "Using $cwd"
    cd $cwd
else
    echo "Using $BLENDER_MAN_EN/locale"
    cd "$BLENDER_MAN_EN/locale"
fi
#latest_file="$HOME/testfile.po"
replaceAllChangedFiles

