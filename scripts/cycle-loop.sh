#!/bin/bash
# Cycle playerctl loop: None → Playlist → Track → None
current=$(playerctl --player=YoutubeMusic loop)
case "$current" in
  None)     playerctl --player=YoutubeMusic loop Playlist ;;
  Playlist) playerctl --player=YoutubeMusic loop Track ;;
  Track)    playerctl --player=YoutubeMusic loop None ;;
esac
