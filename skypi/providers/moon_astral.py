from astral import LocationInfo
from astral.moon import moonrise, moonset, azimuth, elevation, zenith, phase
from zoneinfo import ZoneInfo
import datetime

from ..models import HourlyMoon
from ..config import LATITUDE, LONGITUDE, TIMEZONE

DEBUG = True

"""
https://sffjunkie.github.io/astral/

python -m skypi.providers.moon_astral      

date = date
dt = datetime

"""

# create ASTRAL custom location
city = LocationInfo(
    "Abu Dhabi",
    "UAE",
    TIMEZONE,
    LATITUDE,
    LONGITUDE
)

#ASTRAL city = LocationInfo
observer = city.observer

# helper functions getting specific information
def moon_rise_and_set(target_date):
    m_rise = moonrise(observer, target_date, tzinfo=ZoneInfo(TIMEZONE))
    m_set = moonset(observer, target_date, tzinfo=ZoneInfo(TIMEZONE))
    return m_rise, m_set

def moon_phase(start_date):
    return phase(start_date)

def moon_location(hour_dt_utc):
    az = azimuth(observer, at=hour_dt_utc)
    el = elevation(observer, at=hour_dt_utc)
    ze = zenith(observer, at=hour_dt_utc)
    return az, el, ze

def get_moon_meta(target_date):
    mrise, mset = moon_rise_and_set(target_date)
    moon_phase_value = moon_phase(target_date)
    return mrise, mset, moon_phase_value


# function to return data to use in main programme
def get_hourlymoon(start_dt, end_dt):
   
    hours = []
    current_dt = start_dt


    while current_dt <= end_dt:
        hour_dt_utc = current_dt.astimezone(datetime.timezone.utc)  # fix for astral/UTC issue
        _, el, _ = moon_location(hour_dt_utc)
        ph = moon_phase(current_dt.date())

        hours.append(HourlyMoon(time=current_dt, phase=ph, el=el))
        current_dt += datetime.timedelta(hours=1)

    return hours


if __name__ == "__main__":

    start_dt = datetime.datetime.now(ZoneInfo(TIMEZONE)).replace(minute=0, second=0, microsecond=0)
    end_dt = start_dt + datetime.timedelta(hours=6)
    hours = get_hourlymoon(start_dt, end_dt)
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
