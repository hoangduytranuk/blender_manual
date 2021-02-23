#!/bin/zsh -x
FROM_VIPO=$BLENDER_GITHUB/gui/2.9x/po/vi.po
WITH_POT=$BLENDER_GITHUB/../po/blender.pot
TEMP_FILE=$HOME/msgmerge_out_temp.po
OUT_FILE=$HOME/msgmerge_out.po

msgmerge --no-wrap $FROM_VIPO $WITH_POT -o $TEMP_FILE
msgcat --no-wrap $TEMP_FILE > $OUT_FILE
