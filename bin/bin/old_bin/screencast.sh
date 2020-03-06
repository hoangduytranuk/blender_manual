#!/bin/bash
NAME=$1;
NUMBER=$2;
EXT="mkv";
SEQNO=$(printf "%04d" $NUMBER);
FILE_NAME=$(printf "%s_%s.%s" $NAME $SEQNO $EXT);
CMD="ffmpeg -f x11grab -r 25 -s 1440x900 -i :0.0 -f alsa -i hw:0,0 -acodec flac -vcodec ffvhuff $FILE_NAME"
echo $CMD
$CMD
