#!/usr/bin/env python3
"""Morning Letter weather: hourly + 7-day for Jonesboro, AR.
Primary: Open-Meteo. Backup: National Weather Service (api.weather.gov).
Usage: python3 weather.py [--json]
Prints an HTML-ready table fragment (default) or raw JSON (--json).
Missing values are shown as an em dash, never guessed.
"""
import json, sys, urllib.request, urllib.parse
from datetime import datetime, date

LAT, LON, TZ = 35.8423, -90.7043, "America/Chicago"
HOURS = [6, 9, 12, 15, 18, 21]
PERIODS = {9: "morning", 12: "midday", 15: "afternoon"}
UA = {"User-Agent": "MorningLetter/1.0"}
DASH = "—"


def get(url, tries=3):
    import time, urllib.error
    for n in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503) or n == tries - 1:
                raise
            time.sleep(4 * (n + 1))


def open_meteo():
    q = urllib.parse.urlencode({
        "latitude": LAT, "longitude": LON, "timezone": TZ,
        "temperature_unit": "fahrenheit", "wind_speed_unit": "mph",
        "hourly": "temperature_2m,precipitation_probability,cloud_cover,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
        "forecast_days": 7,
    })
    d = get("https://api.open-meteo.com/v1/forecast?" + q)
    h, dl = d["hourly"], d["daily"]
    today = dl["time"][0]
    hours = []
    for i, t in enumerate(h["time"]):
        if t.startswith(today) and int(t[11:13]) in HOURS:
            hours.append({"hour": int(t[11:13]), "temp": h["temperature_2m"][i],
                          "rain": h["precipitation_probability"][i],
                          "cloud": h["cloud_cover"][i], "wind": h["wind_speed_10m"][i]})
    days = [{"date": dl["time"][i], "high": dl["temperature_2m_max"][i],
             "low": dl["temperature_2m_min"][i],
             "rain": dl["precipitation_probability_max"][i],
             "code": dl["weather_code"][i]} for i in range(len(dl["time"]))]
    per = {}
    for i, t in enumerate(h["time"]):
        hr = int(t[11:13])
        if hr in PERIODS:
            per.setdefault(t[:10], {})[PERIODS[hr]] = {
                "temp": h["temperature_2m"][i], "rain": h["precipitation_probability"][i],
                "cloud": h["cloud_cover"][i]}
    return {"source": "Open-Meteo", "date": today, "hours": hours, "days": days, "periods": per}


def nws():
    pt = get(f"https://api.weather.gov/points/{LAT},{LON}")["properties"]
    hrs = get(pt["forecastHourly"])["properties"]["periods"]
    today = date.today().isoformat()
    per = {}
    for p in hrs:
        t = p["startTime"]
        if int(t[11:13]) in PERIODS:
            per.setdefault(t[:10], {})[PERIODS[int(t[11:13])]] = {
                "temp": p["temperature"],
                "rain": (p.get("probabilityOfPrecipitation") or {}).get("value"),
                "cloud": p.get("shortForecast")}
    hours = []
    for p in hrs:
        t = p["startTime"]
        if t.startswith(today) and int(t[11:13]) in HOURS:
            hours.append({"hour": int(t[11:13]), "temp": p["temperature"],
                          "rain": (p.get("probabilityOfPrecipitation") or {}).get("value"),
                          "cloud": p.get("shortForecast"), "wind": None})
    days = []
    fper = get(pt["forecast"])["properties"]["periods"]
    lows = {}
    for p in fper:
        if not p["isDaytime"]:
            lows[p["startTime"][:10]] = p["temperature"]
    for p in fper:
        if p["isDaytime"]:
            dt = p["startTime"][:10]
            days.append({"date": dt, "high": p["temperature"], "low": lows.get(dt),
                         "rain": (p.get("probabilityOfPrecipitation") or {}).get("value"),
                         "code": None})
    return {"source": "NWS", "date": today, "hours": hours, "days": days, "periods": per}


def fetch():
    for fn in (open_meteo, nws):
        try:
            data = fn()
            if data["hours"] and data["days"]:
                return data
        except Exception as e:
            print(f"# {fn.__name__} failed: {e}", file=sys.stderr)
    return {"source": None, "date": date.today().isoformat(), "hours": [], "days": []}


def fmt(v, suffix=""):
    return DASH if v is None else f"{round(v)}{suffix}"


def clock(h):
    return f"{h % 12 or 12} {'AM' if h < 12 else 'PM'}"


def sky(c):
    if c is None: return DASH
    if isinstance(c, str): return c
    return "Clear" if c < 20 else "Mostly sunny" if c < 50 else "Partly cloudy" if c < 80 else "Cloudy"


def html(d):
    out = ['<table class="wx">',
           "<tr><th>Hour</th>" + "".join(f"<th>{clock(h['hour'])}</th>" for h in d["hours"]) + "</tr>",
           "<tr><td>Temp</td>" + "".join(f"<td>{fmt(h['temp'], '&deg;')}</td>" for h in d["hours"]) + "</tr>",
           "<tr><td>Sky</td>" + "".join(f"<td>{sky(h['cloud'])}</td>" for h in d["hours"]) + "</tr>",
           "<tr><td>Rain</td>" + "".join(f"<td>{fmt(h['rain'], '%')}</td>" for h in d["hours"]) + "</tr>",
           "</table>",
           '<table class="wx7">',
           "<tr><th></th>" + "".join(
               f"<th>{datetime.fromisoformat(x['date']).strftime('%a %-d')}</th>" for x in d["days"]) + "</tr>",
           "<tr><td>High</td>" + "".join(f"<td>{fmt(x['high'], '&deg;')}</td>" for x in d["days"]) + "</tr>",
           "<tr><td>Low</td>" + "".join(f"<td>{fmt(x['low'], '&deg;')}</td>" for x in d["days"]) + "</tr>",
           "<tr><td>Rain</td>" + "".join(f"<td>{fmt(x['rain'], '%')}</td>" for x in d["days"]) + "</tr>",
           "</table>",
           f'<p class="src">Source: {d["source"] or DASH}, {d["date"]}.</p>']
    return "\n".join(out)


if __name__ == "__main__":
    data = fetch()
    print(json.dumps(data, indent=1) if "--json" in sys.argv else html(data))
