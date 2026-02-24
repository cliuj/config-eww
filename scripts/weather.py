#!/usr/bin/env python3
"""Fetch weather from wttr.in and output JSON with icon and temperature."""
import json
import urllib.request

SVG_DIR = "svg/weather"

WEATHER_SVGS = {
    113: "weather-clear-svgrepo-com.svg",
    116: "weather-few-clouds-svgrepo-com.svg",
    119: "weather-overcast-svgrepo-com.svg",
    122: "weather-overcast-svgrepo-com.svg",
    143: "weather-fog-svgrepo-com.svg",
    176: "weather-showers-scattered-svgrepo-com.svg",
    179: "weather-snow-svgrepo-com.svg",
    182: "weather-showers-svgrepo-com.svg",
    185: "weather-showers-svgrepo-com.svg",
    200: "weather-storm-svgrepo-com.svg",
    227: "weather-snow-svgrepo-com.svg",
    230: "weather-snow-svgrepo-com.svg",
    248: "weather-fog-svgrepo-com.svg",
    260: "weather-fog-svgrepo-com.svg",
    263: "weather-showers-scattered-svgrepo-com.svg",
    266: "weather-showers-scattered-svgrepo-com.svg",
    293: "weather-showers-scattered-svgrepo-com.svg",
    296: "weather-showers-scattered-svgrepo-com.svg",
    299: "weather-showers-svgrepo-com.svg",
    302: "weather-showers-svgrepo-com.svg",
    305: "weather-showers-svgrepo-com.svg",
    308: "weather-showers-svgrepo-com.svg",
    311: "weather-showers-svgrepo-com.svg",
    314: "weather-showers-svgrepo-com.svg",
    317: "weather-showers-svgrepo-com.svg",
    320: "weather-snow-svgrepo-com.svg",
    323: "weather-snow-svgrepo-com.svg",
    326: "weather-snow-svgrepo-com.svg",
    329: "weather-snow-svgrepo-com.svg",
    332: "weather-snow-svgrepo-com.svg",
    335: "weather-snow-svgrepo-com.svg",
    338: "weather-snow-svgrepo-com.svg",
    350: "weather-showers-svgrepo-com.svg",
    353: "weather-showers-scattered-svgrepo-com.svg",
    356: "weather-showers-svgrepo-com.svg",
    359: "weather-showers-svgrepo-com.svg",
    362: "weather-showers-svgrepo-com.svg",
    365: "weather-showers-svgrepo-com.svg",
    368: "weather-snow-svgrepo-com.svg",
    371: "weather-snow-svgrepo-com.svg",
    374: "weather-showers-svgrepo-com.svg",
    377: "weather-showers-svgrepo-com.svg",
    386: "weather-storm-svgrepo-com.svg",
    389: "weather-storm-svgrepo-com.svg",
    392: "weather-storm-svgrepo-com.svg",
    395: "weather-storm-svgrepo-com.svg",
}

DEFAULT_SVG = "weather-few-clouds-svgrepo-com.svg"
FALLBACK = json.dumps({"icon": f"{SVG_DIR}/{DEFAULT_SVG}", "temp": "--", "condition": "Unknown"})


def main():
    try:
        req = urllib.request.Request(
            "https://wttr.in/?format=j1",
            headers={"User-Agent": "eww-weather"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())

        current = data["current_condition"][0]
        temp = current["temp_F"]
        code = int(current["weatherCode"])
        condition = current["weatherDesc"][0]["value"]
        svg = WEATHER_SVGS.get(code, DEFAULT_SVG)

        print(json.dumps({"icon": f"{SVG_DIR}/{svg}", "temp": f"{temp}°F", "condition": condition}))
    except Exception:
        print(FALLBACK)


if __name__ == "__main__":
    main()
