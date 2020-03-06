#!/bin/bash
DIR=$1
cd $DIR
#cd $BLENDER_MAN_VI/LC_MESSAGES
for pofile in $(find . -name "*.po" -print); do
#    perl -0777 -i.original -pe 's/#, fuzzy\nmsgid \"\"\n\"\"/#, fuzzy\nmsgid \"\"\nmsgstr\"\"/igs' $pofile
	shasum_before=$(cat $pofile | sha256sum |  awk '{ print $1 }')
    #perl -0777 -i.original -pe 's/#, fuzzy\nmsgid \"\"\n\"\"/#, fuzzy\nmsgid \"\"\nmsgstr \"\"/igs' $pofile
    #perl -0777 -i.original -pe 's|#, fuzzy\nmsgstr \"\"\n|#, fuzzy\nmsgid \"\"\nmsgstr \"\"\n|igs' $pofile

    sed -i -e 's|Đầu vào giá trị tiêu chuẩn|Đầu vào tiêu chuẩn của giá trị|g' $pofile
    sed -i -e 's|Đầu ra giá trị tiêu chuẩn|Đầu ra tiêu chuẩn của giá trị|g' $pofile
    #sed -i -e 's|chỉ mục|chỉ số|g' $pofile

    #shasum_after=$(perl -0777 -pe 's|#, fuzzy\nmsgstr \"\"\n|#, fuzzy\nmsgid \"\"\nmsgstr \"\"\n|igs' $pofile | sha256sum | awk '{ print $1 }')
    #perl -0777 -i.original -pe 's/#, fuzzy\nmsgstr \"\"\n\"Project/#, fuzzy\nmsgid \"\"\nmsgstr \"\"\n\"Project/igs' $pofile
	shasum_after=$(sha256sum $pofile |  awk '{ print $1 }')
	if [ "$shasum_before" != "$shasum_after" ]; then
		echo "Replaced: $pofile"
	fi
done
