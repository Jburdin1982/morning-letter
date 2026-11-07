#!/usr/bin/env python3
"""Deer-movement and fishing outlook for Jonesboro, AR. Usage: outdoors.py YYYY-MM-DD > out.json
A rule-of-thumb ESTIMATE from weather (Open-Meteo), sunrise/sunset (astral) and the rut calendar.
Ratings: Poor / Fair / Good / Excellent. Never invents data: returns nulls when weather is missing."""
import sys, json, time, datetime as dt, urllib.request, urllib.error
from astral import LocationInfo
from astral.sun import sun
import zoneinfo

LAT, LON = 35.8423, -90.7043
TZ = zoneinfo.ZoneInfo("America/Chicago")
RATING = ["Poor", "Fair", "Good", "Excellent"]

def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MorningLetter/1.0"})
            return json.load(urllib.request.urlopen(req, timeout=25))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < tries - 1:
                time.sleep(4 * (i + 1)); continue
            raise
        except Exception:
            if i < tries - 1:
                time.sleep(4 * (i + 1)); continue
            raise

def band(score):
    return RATING[0 if score <= 0 else 1 if score <= 2 else 2 if score <= 4 else 3]

def rut_phase(d):
    """NE Arkansas (Delta/Crowley's Ridge): AGFC puts the average statewide peak ~Nov 11, north AR ~Nov 13,
    Delta later (mid-late Nov). Treat Nov 8-25 as peak window."""
    md = (d.month, d.day)
    if (11, 8) <= md <= (11, 25): return 2, "peak rut window"
    if (10, 28) <= md <= (11, 7): return 1, "pre-rut (bucks starting to cruise)"
    if (11, 26) <= md <= (12, 10): return 1, "late rut / post-peak chasing"
    return 0, "outside the main rut"

def main():
    date = dt.date.fromisoformat(sys.argv[1])
    s = sun(LocationInfo("Jonesboro", "USA", "America/Chicago", LAT, LON).observer, date=date, tzinfo=TZ)
    out = {"date": str(date), "sunrise": s["sunrise"].strftime("%-I:%M %p"), "sunset": s["sunset"].strftime("%-I:%M %p"),
           "weather": None, "deer": None, "fish": None}
    rf, phase = rut_phase(date)
    try:
        u = ("https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s&timezone=America/Chicago"
             "&temperature_unit=fahrenheit&wind_speed_unit=mph&forecast_days=3&past_days=1"
             "&hourly=temperature_2m,pressure_msl,wind_speed_10m,cloud_cover,precipitation_probability" % (LAT, LON))
        h = get(u)["hourly"]
    except Exception as e:
        out["error"] = "weather unavailable: %s" % e
        out["deer"] = {"rating": None, "rut_phase": phase}
        print(json.dumps(out)); return
    times = h["time"]
    def at(day, hour, key):
        t = "%sT%02d:00" % (day, hour)
        return h[key][times.index(t)] if t in times else None
    d0 = str(date); dm1 = str(date - dt.timedelta(days=1))
    # pressure change: 6am today vs 6am previous (if available) else vs 18h ahead
    p6 = at(d0, 6, "pressure_msl"); p18 = at(d0, 18, "pressure_msl"); p_next = at(str(date + dt.timedelta(days=1)), 6, "pressure_msl")
    p_dawn_prev = at(dm1, 6, "pressure_msl")
    dp24 = (p6 - p_dawn_prev) if (p6 is not None and p_dawn_prev is not None) else None
    dp_day = (p18 - p6) if (p6 is not None and p18 is not None) else None
    temp_dawn = at(d0, 6, "temperature_2m"); temp_aft = at(d0, 15, "temperature_2m")
    temp_dawn_prev = at(dm1, 6, "temperature_2m")
    wind_am = at(d0, 8, "wind_speed_10m"); wind_pm = at(d0, 16, "wind_speed_10m")
    cloud = at(d0, 12, "cloud_cover")
    rain = max([x for x in [at(d0, hh, "precipitation_probability") for hh in range(6, 21, 3)] if x is not None] or [0])
    inhg = lambda hpa: round(hpa * 0.02953, 2) if hpa is not None else None
    out["weather"] = {"dawn_temp": temp_dawn, "afternoon_temp": temp_aft, "wind_morning_mph": wind_am, "wind_evening_mph": wind_pm,
                      "cloud_noon": cloud, "rain_chance_max": rain, "pressure_inhg_dawn": inhg(p6),
                      "pressure_change_24h_inhg": round(dp24 * 0.02953, 2) if dp24 is not None else None,
                      "pressure_change_day_inhg": round(dp_day * 0.02953, 2) if dp_day is not None else None}
    # ---- DEER ----
    score = rf; why = ["rut: " + phase]
    if temp_dawn is not None:
        if temp_dawn <= 45: score += 1; why.append("cool dawn (%d F)" % round(temp_dawn))
        elif temp_dawn >= 65: score -= 2; why.append("warm dawn (%d F)" % round(temp_dawn))
    if dp24 is not None:
        if dp24 >= 3: score += 1; why.append("pressure rising after a front")
    if dp_day is not None and dp_day <= -2: score += 1; why.append("pressure falling (deer feed ahead of weather)")
    if temp_dawn is not None and temp_dawn_prev is not None and temp_dawn_prev - temp_dawn >= 8:
        score += 1; why.append("sharp cool-down from yesterday")
    wmax = max([w for w in (wind_am, wind_pm) if w is not None] or [0])
    if wmax >= 18: score -= 1; why.append("gusty wind (%d mph)" % round(wmax))
    elif wmax <= 8: why.append("light wind")
    if rain >= 70: score -= 1; why.append("heavy rain likely")
    out["deer"] = {"rating": band(score), "score": score, "rut_phase": phase, "reasons": why,
                   "windows": {"morning": "%s to about 2 hours after" % (s["sunrise"] - dt.timedelta(minutes=30)).strftime("%-I:%M %p"),
                               "evening": "%s to %s" % ((s["sunset"] - dt.timedelta(hours=2)).strftime("%-I:%M %p"), s["sunset"].strftime("%-I:%M %p")),
                               "midday": "10 AM to 2 PM is realistic (bucks cruising)" if rf == 2 else None}}
    # ---- FISH (Crowley's Ridge lakes: bass, crappie, bream, catfish) ----
    fs = 1; fw = []
    if dp24 is not None:
        if abs(dp24) <= 2: fs += 1; fw.append("steady pressure")
        elif dp24 <= -4: fs -= 1; fw.append("pressure dropping fast")
    if dp_day is not None and -4 < dp_day <= -1.5: fs += 1; fw.append("slow fall ahead of weather (fish feed)")
    if temp_dawn is not None and temp_dawn_prev is not None and temp_dawn_prev - temp_dawn >= 10:
        fs -= 1; fw.append("cold snap just arrived")
    if temp_aft is not None and temp_aft >= 55: fs += 1; fw.append("warm afternoon (%d F)" % round(temp_aft))
    if cloud is not None and cloud >= 60: fs += 0; fw.append("overcast")
    wf = max([w for w in (wind_am, wind_pm) if w is not None] or [0])
    if 5 <= wf <= 12: fs += 1; fw.append("light chop")
    elif wf >= 18: fs -= 1; fw.append("windy")
    out["fish"] = {"rating": band(fs), "score": fs, "reasons": fw,
                   "best": "late morning through mid-afternoon as the water warms; a second window in the last hour before sunset (%s)" % s["sunset"].strftime("%-I:%M %p")}
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
