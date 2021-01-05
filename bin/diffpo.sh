#!/bin/zsh -x
# from_file=$HOME/po/po/blender.pot
from_file=$HOME/po/po/blender.pot
to_file=$HOME/blender_manual/gui/2.9x/po/vi.po
out_file=$HOME/diffpo.txt
msg_cat_out=$HOME/diffpo.po
diff -iEbwBy $from_file $to_file > $out_file
msgcat --no-wrap $from_file $to_file -o $msg_cat_out