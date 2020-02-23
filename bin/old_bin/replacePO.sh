#!/bin/bash
YOUR_NAME="my name in full"
YOUR_EMAIL="myemailname@someserver.com"
YOUR_ID="$YOUR_NAME <$YOUR_EMAIL>"
YOUR_TRANSLATION_TEAM="Your Team Name, City, Town"
YOUR_TRANSLATION_TEAM_EMAIL="$YOUR_EMAIL"
YOUR_LANGUAGE_CODE="vi"

# FIRST AUTHOR <EMAIL@ADDRESS>, 2018.
#"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
#"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
#"Language-Team: LANGUAGE <LL@li.org>\n"
#"Language: vi\\n"
#"MIME-Version: 1.0\n"
#"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"

date_bin=/usr/bin/date
time_now=$($date_bin +"%F %H:%M%z")
#FIRST_AUTHOR=("FIRST AUTHOR.*SS>" "$YOUR_ID")
#LAST_TRANSLATOR=("Last-Translator.*>" "Last-Translator: $YOUR_ID")
#PO_REVISION_DATE_FILLED=("PO-Revision-Date: [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\+[0-9]{4}" "PO-Revision-Date: $time_now")
#PO_REVISION_DATE_NON_FILLED=("PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE" "PO-Revision-Date: $time_now")
#LANGUAGE_TEAM=("Language-Team:.*>" "Language-Team: <$YOUR_TRANSLATION_TEAM_EMAIL>")
#LANGUAGE_CODE=("\"MIME-Version" "\"Language: vi\\\\n\"\n\"\"MIME-Version")

declare -A pattern_list=(
["FIRST AUTHOR.*SS>"]="$YOUR_ID"
["Last-Translator.*>"]="$YOUR_ID"
["PO-Revision-Date: [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\+[0-9]{4}"]="PO-Revision-Date: ${time_now}"
["PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE"]="PO-Revision-Date: ${time_now}"
["Language-Team:.*>"]="Language-Team: <$YOUR_TRANSLATION_TEAM_EMAIL>"
["\"MIME-Version"]="\"Language: vi\\\\n\"\n\"\"MIME-Version"
)

test_file="$HOME/testfile.po"
#sed -i "s|${FIRST_AUTHOR[0]}|${FIRST_AUTHOR[1]}|g" $test_file
#sed -i "s|${LAST_TRANSLATOR[0]}|${LAST_TRANSLATOR[1]}|g" $test_file
#sed -i "s|${PO_REVISION_DATE_FILLED[0]}|${PO_REVISION_DATE_FILLED[1]}|g" $test_file
#sed -i "s|${PO_REVISION_DATE_NON_FILLED[0]}|${PO_REVISION_DATE_NON_FILLED[1]}|g" $test_file
#sed -i "s|${LANGUAGE_TEAM[0]}|${LANGUAGE_TEAM[1]}|g" $test_file
#sed -i "s|${LANGUAGE_CODE[0]}|${LANGUAGE_CODE[1]}|g" $test_file
#cat $test_file

#cmdline=""
#$cmdline

for i in "${!pattern_list[@]}"; do
    #printf "%s\t%s\n" "$i" "${pattern_list[$i]}"
    pattern="$i"
    value="${pattern_list[$i]}"
    echo "$pattern => $value"
    sed -i "s|${pattern}|${value}|g" $test_file
done
cat $test_file
