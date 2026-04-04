from datetime import date
from pathlib import Path

from .astro_sessions import get_astro_sessions, get_next_good_astro
from ..utils.moon import get_moon_phase_image

from .evaluator import get_evaluations
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


def calc_best_window_avgs(best_hours,rating):
    cloud_vals = []
    visibility_vals = []

    if rating["rag"] == "R":
        best_avgs = {
            "avg_cloud" : "-",
            "avg_visibility" : "-",
        }
    
    else:
        for hour in best_hours:
            cloud_vals.append(hour.cloud_pct)
            visibility_vals.append(hour.visibility_m)

        cloud_avg = sum(cloud_vals)/len(cloud_vals)
        visibility_avg = sum(visibility_vals)/len(visibility_vals)

        best_avgs = {
            "avg_cloud" : cloud_avg,
            "avg_visibility" : visibility_avg,
        }

    return best_avgs


def summary_moon_data(todays_astro_hours):
    moon_hours = []
    moon_phase = todays_astro_hours[0].moon_phase
    moon_phase_image = get_moon_phase_image(moon_phase)

    
    for i, hr in enumerate(todays_astro_hours):
        hr_el = hr.moon_elevation

        # rating
        if hr_el >= 5:
            rating = "R"
        elif -18 <= hr_el < 5:
            rating = "A"
        else:
            rating = "G"

        # label
        hour_label = hr.time.strftime("%H")

        # position (simple spacing)
        left_positions = [5, 20, 35, 50, 65, 80, 95]
        left_pct = left_positions[i]

        # height scaling
        height_pct = abs(hr_el) / 90

        moon_hour = {
            "hour_label": hour_label,
            "elevation": hr_el,
            "rating": rating,
            "left_pct": left_pct,
            "height_pct": height_pct,
        }

        moon_hours.append(moon_hour)

    return {
        "moon_phase_image" : moon_phase_image,
        "moon_hours" : moon_hours,

    }



def get_daily_report():
    # get forecast data grouped by astro session
    astro_session_data = get_astro_sessions()
    
    # extract day 0 (todays) overall rating
    go_no_go = astro_session_data[0].astro_rating

    # use day 0 data to return todays "at a glance"
    at_a_glance = tonight_at_a_glance(astro_session_data[0].astro_hours)

    # get moon summary info
    summary_moon = summary_moon_data(astro_session_data[0].astro_hours)

    # get next good session
    next_good_night = get_next_good_astro(astro_session_data)

    # unpack astro_sessions and extract all hourly forecasts
    hourly_breakdown = []
    for session in astro_session_data:
        hourly_breakdown.extend(session.astro_hours)


    return {
        "go_no_go": go_no_go, 
        "at_a_glance": at_a_glance,
        "summary_moon" : summary_moon,
        "next_good_night" : next_good_night,
        "astro_session_data": astro_session_data,
    }


if __name__ == "__main__":
    """
    python -m skypi.services.daily_report
    """
    report = get_daily_report()
    print(report)