from datetime import date

from .forecaster import get_forecast_data

from ..evaluator import get_evaluations
from ..utils.moon import get_moon_position, get_moon_phase

from ..config import START_TIME, END_TIME

""""""
# REMOVE IN REFACTOR
from ..providers.weather_openmeteo import get_hourly_forecast
from ..providers.moon_astral import get_hourlymoon
""""""


# add milkyway position
# potentially later DSO/Constellation location


# def moon_position(altitude):
#     if altitude > 0:
#         moon_display = f" ↑ {altitude:.0f}°"
#     else:
#         moon_display = f" ↓ {abs(altitude):.0f}°"
#         if abs(altitude) >= 18:
#             moon_display += " ✨"

#     return(moon_display)


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


def get_daily_report():
    # get forecast data
    today = date.today().isoformat()

    hourly_forecast = get_forecast_data()

    # turn data into information
    go_no_go, hours = get_evaluations(hourly_forecast)
    at_a_glance = tonight_at_a_glance(hourly_forecast)

    return {
        "go_no_go": go_no_go, 
        "at_a_glance": at_a_glance,
        "hours": hours
    }
