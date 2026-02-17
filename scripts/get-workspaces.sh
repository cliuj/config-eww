#!/bin/bash
SCREEN=${1:-0}

# Icon mapping (Nerd Font)
icon_for() {
    case "$1" in
    term) printf '\uf120' ;;
    code) printf '\uf121' ;;
    browser) printf '\uf0ac' ;;
    comm) printf '\uf086' ;;
    *) printf '%s' "$1" ;;
    esac
}

xprop -notype -spy -root 8t "_XMONAD_LOG_$SCREEN" | while IFS= read -r line; do
    # Strip property prefix: '_XMONAD_LOG_0 = "..."' → content between quotes
    raw=$(echo "$line" | sed 's/.*= "//;s/"$//')

    # Split on ||| → workspaces part and layout part
    ws_part=$(echo "$raw" | sed 's/|||.*//')
    layout=$(echo "$raw" | sed 's/.*|||//')

    # Sort workspace entries by index so display order is stable
    IFS='|' read -ra entries <<<"$ws_part"
    sorted=$(for entry in "${entries[@]}"; do
        [ -z "$entry" ] && continue
        echo "$entry"
    done | sort -t: -k3 -n)

    # Parse sorted entries into JSON array
    json='{"layout":"'"$layout"'","workspaces":['
    first=true
    while IFS= read -r entry; do
        [ -z "$entry" ] && continue
        state=$(echo "$entry" | cut -d: -f1)
        name=$(echo "$entry" | cut -d: -f2)
        idx=$(echo "$entry" | cut -d: -f3)
        icon=$(icon_for "$name")

        $first || json+=','
        first=false
        json+='{"state":"'"$state"'","name":"'"$name"'","icon":"'"$icon"'","index":'"$idx"'}'
    done <<<"$sorted"
    json+=']}'

    echo "$json"
done
