#!/usr/bin/env python3
"""Send a command to XMonad via ServerMode X client message."""
import sys
from Xlib import X, display
from Xlib.protocol import event

def send_command(cmd: str):
    dpy = display.Display()
    root = dpy.screen().root
    atom = dpy.intern_atom("XMONAD_COMMAND")

    # Encode command index: serverModeEventHookCmd' uses the atom value
    # We send a ClientMessage with the command string as an atom
    cmd_atom = dpy.intern_atom(cmd)

    e = event.ClientMessage(
        window=root,
        client_type=atom,
        data=(32, [cmd_atom, 0, 0, 0, 0]),
    )
    root.send_event(e, event_mask=X.SubstructureRedirectMask)
    dpy.flush()

if __name__ == "__main__":
    send_command(sys.argv[1] if len(sys.argv) > 1 else "next-layout")
