#!/bin/bash

RE_COMMENTED_LINE="^#~.*$"

#Remove all commented line after update_po is executed
#find in all directories just in case old files are still there.
function removeCommentedLineInAllFiles()
{
    po_file_list=$(find . -type f -name "*.po")
    for f in ${po_file_list}; do
		removeCommentedLineInSingleFile $f
    done
}

#Remove commented line in a single file
function removeCommentedLineInSingleFile()
{
	orig_file=$1
	tempfile="temp_file.po"
	exclude_lines=$(grep "$RE_COMMENTED_LINE" $orig_file)
    if [ ! -z "$exclude_lines" ]; then
        echo "Removing commented lines from [$orig_file]."
		grep -v "$RE_COMMENTED_LINE" $orig_file > $tempfile
        mv $tempfile $orig_file
	fi
}

removeCommentedLineInAllFiles
