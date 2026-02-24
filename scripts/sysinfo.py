#!/usr/bin/env python3
"""Poll CPU usage and RAM, output JSON."""
import json
import time


def read_cpu_times():
    """Read aggregate CPU times from /proc/stat (first 'cpu' line = all cores combined)."""
    with open("/proc/stat") as f:
        parts = f.readline().split()
    # user, nice, system, idle, iowait, irq, softirq, steal
    times = [int(x) for x in parts[1:9]]
    idle = times[3] + times[4]  # idle + iowait
    total = sum(times)
    return idle, total


def get_ram():
    """Read RAM from /proc/meminfo, return (used_gb, total_gb)."""
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            key, val = line.split(":")
            info[key.strip()] = int(val.split()[0])  # value in kB
    total = info["MemTotal"]
    available = info["MemAvailable"]
    used = total - available
    return used / 1048576, total / 1048576  # kB -> GB


def main():
    idle1, total1 = read_cpu_times()
    time.sleep(0.5)
    idle2, total2 = read_cpu_times()

    idle_delta = idle2 - idle1
    total_delta = total2 - total1
    cpu_pct = round((1 - idle_delta / total_delta) * 100) if total_delta else 0

    ram_used, ram_total = get_ram()

    print(json.dumps({
        "cpu": cpu_pct,
        "ram_used": f"{ram_used:.1f}",
        "ram_total": f"{ram_total:.1f}",
    }))


if __name__ == "__main__":
    main()
