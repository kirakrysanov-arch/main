#!/bin/sh
# Builds a 12-second Etsy listing video from the listing images. Run: sh make_video.sh
set -e
dir="$(dirname "$0")/../listing"
set -- "$dir"/images/0*.jpg
inputs=""; for f in "$@"; do inputs="$inputs -loop 1 -t 2.2 -i $f"; done
# Chain crossfades: each image holds for 1.7s, then fades for 0.5s into the next.
filter=""; prev="0:v"; off=1.7; i=1
while [ $i -lt $# ]; do
  filter="$filter[$prev][$i:v]xfade=transition=fade:duration=0.5:offset=$off[v$i];"
  prev="v$i"; off=$(echo "$off + 1.7" | bc); i=$((i + 1))
done
ffmpeg -y -loglevel error $inputs -filter_complex "${filter}[$prev]scale=1600:1200,format=yuv420p[out]" \
  -map "[out]" -c:v libx264 -preset slow -crf 20 -r 30 -an -movflags +faststart "$dir/images/listing-video.mp4"
