from datetime import date

from .forecaster import get_forecast
from .astro_sessions import get_astro_sessions

from ..evaluator import get_evaluations
from ..utils.moon import get_moon_position, get_moon_phase

from ..config import START_TIME, END_TIME


# add milkyway position
# potentially later DSO/Constellation location


def tonight_at_a_glance(hourly_forecast):
    # work out ranges to display
    all_cloud = []
    all_wind = []
    all_visibility = []
    all_temp = []
    all_rain = []
    all_moon = []

    # weather elements
    for hr in hourly_forecast:
        all_cloud.append(hr.cloud_pct)
        all_wind.append(hr.wind_kmh)
        all_visibility.append(hr.visibility_m)
        all_temp.append(hr.temp_c)
        all_rain.append(hr.rain_pct)
        all_moon.append(hr.moon_elevation)

    cloud_range = f"{min(all_cloud)} - {max(all_cloud)}%"
    wind_range = f"{min(all_wind)} - {max(all_wind)} km/h"
    visibility_range = f"{min(all_visibility)/1000:.0f} - {max(all_visibility)/1000:.0f} km"
    temp_range = f"{min(all_temp)} - {max(all_temp)}°C"
    if min(all_rain) == 0:
        rain_range = f"{max(all_rain)}%"
    else:
        rain_range = f"{min(all_rain)} - {max(all_rain)}%"


    moon_phase = get_moon_phase(hourly_forecast[0].moon_phase)
    moon_start_alt = hourly_forecast[0].moon_elevation
    moon_end_alt = hourly_forecast[-1].moon_elevation

    moon_start = get_moon_position(moon_start_alt)
    moon_end = get_moon_position(moon_end_alt)

    moon_range = f"{moon_phase} {moon_start} - {moon_end}"

    # package up to return
    return {
        "cloud_range": cloud_range,
        "wind_range": wind_range,
        "visibility_range": visibility_range,
        "temp_range": temp_range,
        "rain_range": rain_range,
        "moon_range": moon_range,
    }


def next_three_days(astro_forecast_data):

    # make dict of required values
    next_three_days_data = []
    for session in astro_forecast_data:
        first_hour = session.astro_hours[0]

        moon_phase = get_moon_phase(first_hour.moon_phase)
        moon_position = get_moon_position(first_hour.moon_elevation)

        day = {
            "date" : session.astro_date.strftime("%a %d %b"),
            "rating" : session.astro_rating,
            "moon" : (f"{moon_phase} {moon_position}"),
         #   "cloud" : session.astro_hours_hour.cloud_pct,
         #   "visibility" : session.astro_hours_visibility_m
        }
        next_three_days_data.append(day)


    return next_three_days_data
   


def get_daily_report():
    # get forecast data grouped by astro session
    astro_forecast_data = get_astro_sessions()
    
    # extract day 0 (todays) overall rating
    go_no_go = astro_forecast_data[0].astro_rating

    # use day 0 data to return todays "at a glance"
    at_a_glance = tonight_at_a_glance(astro_forecast_data[0].astro_hours)

    # get next three (astro) days forecast
    next_iii_days = next_three_days(astro_forecast_data[1:4])

    # unpack astro_sessions and extract all hourly forecasts
    hourly_breakdown = []
    for session in astro_forecast_data:
        hourly_breakdown.extend(session.astro_hours)


    return {
        "go_no_go": go_no_go, 
        "at_a_glance": at_a_glance,
        "hourly_breakdown": hourly_breakdown,
        "next_three_days" : next_iii_days
    }


if __name__ == "__main__":
    """python -m skypi.services.daily_report"""
    report = get_daily_report()
    print(report)