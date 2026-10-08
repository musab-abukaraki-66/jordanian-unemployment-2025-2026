#!/bin/bash
for n in "$@"; do b=$(basename $n .svg); "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,900 --screenshot="$(cygpath -w "$PWD/concepts/$b.png")" "file:///$(cygpath -m "$PWD")/concepts/$b.svg" >/dev/null 2>&1; done
