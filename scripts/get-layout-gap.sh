#!/bin/bash
SCREEN=${1:-0}

xprop -notype -spy -root 8t "_XMONAD_LOG_$SCREEN" | while IFS= read -r line; do
  raw=$(echo "$line" | sed 's/.*= "//;s/"$//')
  layout=$(echo "$raw" | sed 's/.*|||//')

  case "$layout" in
    BSP|Monocle)          echo 40 ;;
    Tall|"Mirror Tall")   echo 30 ;;
    Fullscreen)           echo 0 ;;
    *)                    echo 40 ;;
  esac
done
