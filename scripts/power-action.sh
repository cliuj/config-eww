#!/bin/sh
# Usage: power-action.sh <action>
# action: suspend | reboot | poweroff
systemctl "$1"
