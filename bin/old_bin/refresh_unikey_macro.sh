#!/bin/bash
pkill -o ibus-engine-uni
cp -a ~/Documents/nondup_macro.txt ~/.ibus/unikey/macro
chmod 664 ~/.ibus/unikey/macro
/usr/ibus-engine-unikey --ibus &
