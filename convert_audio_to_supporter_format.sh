#!/bin/bash

set -e

outfile="$(date "+%F %T").webm"

ffmpeg -i "$1" -c:a libopus -b:a 128k "$outfile"

echo "$outfile"
