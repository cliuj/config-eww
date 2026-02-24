#!/bin/bash
# Poll NetworkManager for connection status. Outputs JSON.

# Check for active wifi connection
wifi_line=$(nmcli -t -f TYPE,STATE,CONNECTION device 2>/dev/null | grep '^wifi:connected:')
if [[ -n "$wifi_line" ]]; then
    name="${wifi_line#wifi:connected:}"
    signal=$(nmcli -t -f IN-USE,SIGNAL dev wifi list 2>/dev/null | grep '^\*:' | head -1 | cut -d: -f2)
    signal=${signal:-0}

    if (( signal >= 75 )); then
        icon="svg/network/wifi.svg"
    elif (( signal >= 50 )); then
        icon="svg/network/wifi-high.svg"
    elif (( signal >= 25 )); then
        icon="svg/network/wifi-low.svg"
    else
        icon="svg/network/wifi-off.svg"
    fi

    printf '{"type":"wifi","state":"connected","name":"%s","signal":%d,"icon":"%s"}\n' \
        "$name" "$signal" "$icon"
    exit 0
fi

# Check for active ethernet connection
eth_line=$(nmcli -t -f TYPE,STATE,CONNECTION device 2>/dev/null | grep '^ethernet:connected:')
if [[ -n "$eth_line" ]]; then
    name="${eth_line#ethernet:connected:}"
    printf '{"type":"ethernet","state":"connected","name":"%s","signal":100,"icon":"svg/network/ethernet-port.svg"}\n' \
        "$name"
    exit 0
fi

# Disconnected
printf '{"type":"none","state":"disconnected","name":"Disconnected","signal":0,"icon":"svg/network/wifi-off.svg"}\n'
