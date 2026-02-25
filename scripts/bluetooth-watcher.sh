#!/bin/bash
# Stream bluetooth status changes. Outputs JSON on each state change.

output_status() {
    local powered="false" connected="false" device="" icon

    if bluetoothctl show 2>/dev/null | grep -q "Powered: yes"; then
        powered="true"
        local dev_line
        dev_line=$(bluetoothctl devices Connected 2>/dev/null | head -1)
        if [[ -n "$dev_line" ]]; then
            connected="true"
            device="${dev_line#Device * }"
            icon="svg/network/bluetooth-signal-svgrepo-com.svg"
        else
            icon="svg/network/bluetooth-on-svgrepo-com.svg"
        fi
    else
        icon="svg/network/bluetooth-slash-svgrepo-com.svg"
    fi

    printf '{"powered":%s,"connected":%s,"device":"%s","icon":"%s"}\n' \
        "$powered" "$connected" "$device" "$icon"
}

# Print initial status
output_status

# Poll every 2 seconds for changes (bluetoothctl has no reliable event stream)
prev=""
while true; do
    sleep 2
    cur=$(output_status)
    if [[ "$cur" != "$prev" ]]; then
        echo "$cur"
        prev="$cur"
    fi
done
