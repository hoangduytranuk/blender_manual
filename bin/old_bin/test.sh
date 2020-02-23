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
["PO-Revision-Date.*[[:digit:]]\{4\}"]="PO-Revision-Date:\ ${time_now}"
#["PO-Revision-Date.*[[:digit:]]\{4\}-[[:digit:]]\{2\}-[[:digit:]]\{2\}.*[[:digit:]]\{2\}:[[:digit:]]\{2\}:[[:digit:]]\{2\}.*[[:digit:]]\{4\}"]="PO-Revision-Date:\ ${time_now}"

)
text_line="\"PO-Revision-Date: 2018-11-09 06:30+0000\n\""
function replaceText()
{
    for i in "${!pattern_list[@]}"; do
        pattern="$i"
        value="${pattern_list[$i]}"
        echo "Replacing: $pattern => $value"
        echo $text_line | sed "s|$pattern|$value|g"
    done
}

replaceText
