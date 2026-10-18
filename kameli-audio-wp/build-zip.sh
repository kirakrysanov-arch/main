#!/bin/sh
# Rakentaa asennettavan teemapaketin: kameli-audio.zip
set -e
cd "$(dirname "$0")"
rm -f kameli-audio.zip
zip -rq kameli-audio.zip kameli-audio -x '*.DS_Store'
echo "Valmis: $(pwd)/kameli-audio.zip"
