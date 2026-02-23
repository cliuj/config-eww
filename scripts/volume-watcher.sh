#!/bin/bash
emit() {
  vol=$(wpctl get-volume @DEFAULT_AUDIO_SINK@)
  pct=$(echo "$vol" | awk '{printf "%d", $2 * 100}')
  muted=$(echo "$vol" | grep -q MUTED && echo "true" || echo "false")
  echo "{\"volume\":$pct,\"muted\":$muted}"
}
emit
pactl subscribe | grep --line-buffered "sink" | while read -r _; do emit; done
