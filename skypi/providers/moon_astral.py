from astral import LocationInfo
from astral.moon import moonrise, moonset, azimuth, elevation, zenith, phase
from zoneinfo import ZoneInfo
import datetime

from ..models import HourlyMoon


# create custom location
city = LocationInfo(
    "Abu Dhabi",
    "UAE",
    "Asia/Dubai",
    23.55053952123817,
    54.74569584563267
)

DEBUG = True

"""
https://sffjunkie.github.io/astral/

"""

#city = LocationInfo
observer = city.observer

# date for rise/set
date = datetime.date.today()

# datetime for position
dt = datetime.datetime(
    date.year,
    date.month,
    date.day,
    19, 0, 0,
    tzinfo=ZoneInfo("Asia/Dubai")
)

def moon_rise_and_set():
    m_rise = moonrise(observer, date, tzinfo="Asia/Dubai")
    m_set = moonset(observer, date, tzinfo="Asia/Dubai")
    return(m_rise, m_set)

def moon_phase():
    return phase(date)

def moon_location(dpt=dt):
    az = azimuth(observer, at=dpt)
    el = elevation(observer, at=dpt)
    ze = zenith(observer, at=dpt)
    return(az,el,ze)

def get_moon_meta():
    mrise, mset = moon_rise_and_set()
    moon_phase_value = moon_phase()
    return (mrise, mset, moon_phase_value)

def get_hourlymoon():
    hours = []

    for i in range(7):
        hour_dt = dt + datetime.timedelta(hours=i)
        hour_dt_utc = hour_dt.astimezone(datetime.timezone.utc) #fix for astral/UTC issue
        _, el,_ = moon_location(hour_dt_utc)   
        ph = moon_phase()
        
        hours.append(HourlyMoon(time=hour_dt.isoformat(), phase=ph, el=el))

    return hours



if __name__ == "__main__":
    m_rise, m_set = moon_rise_and_set()
    az,el,ze = moon_location()
    if DEBUG:
        print("Moonrise:", m_rise)
        print("Moonset:", m_set)

    hours = get_hourlymoon()
    print(hours)


"""
0 .. 6.99       New moon
7 .. 13.99      First quarter
14 .. 20.99     Full moon
21 .. 27.99     Last quarter


What the numbers mean
	•	Azimuth
	•	0° = North
	•	90° = East
	•	180° = South
	•	270° = West
	Elevation
	•	> 0 → moon above horizon
	•	< 0 → moon below horizon
	Zenith
	•	0 = directly overhead
	•	90 = horizon
"""

"""
0 3.5
🌑
3.5–7
🌒
7–10.5
🌓
10.5–14
🌔
14–17.5
🌕
17.5–21
🌖
21–24.5
🌗
24.5–28
🌘

"""
