import sys, json
from datetime import date, datetime, timedelta
from astral import LocationInfo, moon
from astral.sun import sun, dawn, dusk
import zoneinfo
tz = zoneinfo.ZoneInfo("America/Chicago")
loc = LocationInfo("Jonesboro","USA","America/Chicago",35.8423,-90.7043)
d = date.fromisoformat(sys.argv[1])
def f(t): return t.astimezone(tz).strftime("%-I:%M %p")
s = sun(loc.observer, date=d, tzinfo=tz)
y = sun(loc.observer, date=d - timedelta(days=1), tzinfo=tz)
L = s["sunset"] - s["sunrise"]; Ly = y["sunset"] - y["sunrise"]
diff = int((L - Ly).total_seconds())
ph = moon.phase(d)
name = ("New Moon" if ph<1 or ph>27.5 else "Waxing Crescent" if ph<6.4 else "First Quarter" if ph<8.4 else "Waxing Gibbous" if ph<13.4 else "Full Moon" if ph<15.4 else "Waning Gibbous" if ph<20.4 else "Last Quarter" if ph<22.4 else "Waning Crescent")
illum = round((1-__import__('math').cos(2*__import__('math').pi*ph/29.530588))/2*100)
print(json.dumps({"first_light":f(s["dawn"]),"sunrise":f(s["sunrise"]),"noon":f(s["noon"]),"sunset":f(s["sunset"]),"last_light":f(s["dusk"]),
 "day_length":f"{L.seconds//3600} h {L.seconds%3600//60} m","change":f"{'-' if diff<0 else '+'}{abs(diff)//60} m {abs(diff)%60} s","moon":name,"illum":illum,"age":round(ph,1)}))
