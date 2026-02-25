#!/bin/bash
# Stream mullvad VPN status changes. Outputs JSON on each state change.

output_status() {
    local raw state="disconnected" server=""
    raw=$(mullvad status 2>/dev/null | head -1)

    if [[ "$raw" == Connected* ]]; then
        state="connected"
        server="${raw#Connected to }"
    elif [[ "$raw" == Connecting* ]]; then
        state="connecting"
    fi

    printf '{"state":"%s","server":"%s"}\n' "$state" "$server"
}

# Print initial status
output_status

# Listen for changes, debounced to avoid rapid subprocess spawning
last_update=0
mullvad status listen 2>/dev/null | while read -r _line; do
    now=$(date +%s)
    if (( now - last_update >= 1 )); then
        output_status
        last_update=$now
    fi
done
