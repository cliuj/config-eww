#!/usr/bin/env python3
"""Toggle bluetooth adapter power on/off via D-Bus."""

import dbus

bus = dbus.SystemBus()
adapter = dbus.Interface(
    bus.get_object("org.bluez", "/org/bluez/hci0"),
    "org.freedesktop.DBus.Properties",
)
powered = bool(adapter.Get("org.bluez.Adapter1", "Powered"))
adapter.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(not powered))
