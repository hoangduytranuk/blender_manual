#!/bin/bash -x
from_line="Language-Team: London, UK <hoangduytran1960@gmail.com>Plural-Forms: nplurals=1; plural=0\\n"
to_line="Language-Team: London, UK <hoangduytran1960@gmail.com>\\n\"\n\"Plural-Forms: nplurals=1; plural=0\\n"
from_dir=$BLENDER_MAN_VI
from_file=~/community.po
echo $from_line | sed -En 's|\.com>Plu|\.com>\\n\"\\n\"Plu|p'
# file_list=$(find $from_dir -name "*.po" -print | sort)