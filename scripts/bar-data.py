#!/usr/bin/env python3
"""Eww bar data provider — watches xmonad xprop via python-xlib and emits JSON."""
import asyncio
import json
import sys

from Xlib import X, display

ICONS = {"term": "\uf120", "code": "\uf121", "browser": "\uf0ac", "comm": "\uf086"}
GAP_MAP = {"BSP": 40, "Monocle": 40, "Tall": 30, "Mirror Tall": 30, "Fullscreen": 0}


def parse_log(value: str) -> dict:
    ws_part, _, layout = value.partition("|||")
    workspaces = []
    for entry in ws_part.split("|"):
        if not entry:
            continue
        state, name, idx = entry.split(":")
        workspaces.append({"state": state, "name": name,
                           "icon": ICONS.get(name, name), "index": int(idx)})
    workspaces.sort(key=lambda w: w["index"])
    return {"layout": layout, "gap": GAP_MAP.get(layout, 40), "workspaces": workspaces}


def read_property(dpy, root, atom) -> str | None:
    prop = root.get_full_property(atom, X.AnyPropertyType)
    if prop is None:
        return None
    return prop.value.decode() if isinstance(prop.value, bytes) else str(prop.value)


async def watch_xprop(screen: int):
    dpy = display.Display()
    root = dpy.screen().root
    atom = dpy.intern_atom(f"_XMONAD_LOG_{screen}")

    # Subscribe to property changes on root window
    root.change_attributes(event_mask=X.PropertyChangeMask)

    # Emit initial state
    value = read_property(dpy, root, atom)
    if value:
        print(json.dumps(parse_log(value)), flush=True)

    # Event loop — run blocking X11 event reads in a thread
    loop = asyncio.get_event_loop()

    while True:
        # Wait for the X11 fd to be readable
        await loop.run_in_executor(None, lambda: dpy.next_event())
        # Drain any pending events
        while dpy.pending_events():
            dpy.next_event()
        # Re-read the property (coalesce multiple events)
        value = read_property(dpy, root, atom)
        if value:
            print(json.dumps(parse_log(value)), flush=True)


if __name__ == "__main__":
    asyncio.run(watch_xprop(int(sys.argv[1]) if len(sys.argv) > 1 else 0))
