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

# Listen for changes
mullvad status listen 2>/dev/null | while read -r _line; do
    output_status
done
