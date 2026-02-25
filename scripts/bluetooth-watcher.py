#!/usr/bin/env python3
"""Event-based bluetooth status watcher using D-Bus signals."""

import json
import sys

import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

BLUEZ_SERVICE = "org.bluez"
ADAPTER_PATH = "/org/bluez/hci0"
ADAPTER_IFACE = "org.bluez.Adapter1"
DEVICE_IFACE = "org.bluez.Device1"
PROPS_IFACE = "org.freedesktop.DBus.Properties"
OBJ_MANAGER_IFACE = "org.freedesktop.DBus.ObjectManager"

ICON_OFF = "svg/network/bluetooth-slash-svgrepo-com.svg"
ICON_ON = "svg/network/bluetooth-on-svgrepo-com.svg"
ICON_CONNECTED = "svg/network/bluetooth-signal-svgrepo-com.svg"


def get_status(bus):
    try:
        adapter = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE, ADAPTER_PATH), PROPS_IFACE
        )
        powered = bool(adapter.Get(ADAPTER_IFACE, "Powered"))
    except dbus.exceptions.DBusException:
        return {"powered": False, "connected": False, "device": "", "icon": ICON_OFF}

    if not powered:
        return {"powered": False, "connected": False, "device": "", "icon": ICON_OFF}

    # Find connected devices via ObjectManager
    try:
        manager = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE, "/"), OBJ_MANAGER_IFACE
        )
        objects = manager.GetManagedObjects()
        for path, ifaces in objects.items():
            if DEVICE_IFACE in ifaces:
                dev = ifaces[DEVICE_IFACE]
                if dev.get("Connected", False):
                    name = str(dev.get("Alias", dev.get("Name", "Unknown")))
                    return {
                        "powered": True,
                        "connected": True,
                        "device": name,
                        "icon": ICON_CONNECTED,
                    }
    except dbus.exceptions.DBusException:
        pass

    return {"powered": True, "connected": False, "device": "", "icon": ICON_ON}


def emit(bus):
    print(json.dumps(get_status(bus)), flush=True)


def main():
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()

    # Print initial state
    emit(bus)

    # Listen for property changes on any bluez object
    bus.add_signal_receiver(
        lambda *args, **kwargs: emit(bus),
        signal_name="PropertiesChanged",
        dbus_interface=PROPS_IFACE,
        bus_name=BLUEZ_SERVICE,
        path_keyword="path",
    )

    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()


if __name__ == "__main__":
    main()
