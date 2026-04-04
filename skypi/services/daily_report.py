from datetime import date
from pathlib import Path

from .astro_sessions import get_astro_sessions, get_next_good_astro
from ..utils.moon import get_moon_phase_image

from .evaluator import get_evaluations
from ..utils.moon import get_moon_position, get_moon_phase

from ..config import START_TIME, END_TIME


# add milkyway position
# potentially later DSO/Constellation location
# This file shapes the daily UI summary data from the astro session data.
# It does not fetch raw provider data itself.


# Build the simple summary ranges shown in the "Tonight at a glance" block.
def tonight_at_a_glance(hourly_forecast):
    # collect the values we want to turn into simple display ranges
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


    # moon summary just uses the first and last astro hours for the display line
    moon_phase = get_moon_phase(hourly_forecast[0].moon_phase)
    moon_start_alt = hourly_forecast[0].moon_elevation
    moon_end_alt = hourly_forecast[-1].moon_elevation

    moon_start = get_moon_position(moon_start_alt)
    moon_end = get_moon_position(moon_end_alt)

    moon_range = f"{moon_phase} {moon_start} - {moon_end}"

    # package up the summary values for the template
    return {
        "cloud_range": cloud_range,
        "wind_range": wind_range,
        "visibility_range": visibility_range,
        "temp_range": temp_range,
        "rain_range": rain_range,
        "moon_range": moon_range,
    }


# Small helper for best-window averages.
# Not currently used in the main report, but keeping it here for now.
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


# Build the moon-specific summary data for the right-hand summary block.
# This includes the phase image and the tiny elevation chart data.
def summary_moon_data(todays_astro_hours):
    moon_hours = []
    moon_phase = todays_astro_hours[0].moon_phase
    moon_phase_image = get_moon_phase_image(moon_phase)

    
    for i, hr in enumerate(todays_astro_hours):
        hr_el = hr.moon_elevation

        # simple UI rating for the chart bar colour
        if hr_el >= 5:
            rating = "R"
        elif -18 <= hr_el < 5:
            rating = "A"
        else:
            rating = "G"

        # hour label used under the chart
        hour_label = hr.time.strftime("%H")

        # fixed left positions across the mini chart
        left_positions = [5, 20, 35, 50, 65, 80, 95]
        left_pct = left_positions[i]

        # normalise elevation to a 0-1 chart height
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



# Main entry point for the homepage data.
# Pulls together the top-level blocks the template needs.
def get_daily_report():
    # get the forecast already grouped into astro nights
    astro_session_data = get_astro_sessions()
    
    # overall result for tonight
    go_no_go = astro_session_data[0].astro_rating

    # simple weather summary for tonight
    at_a_glance = tonight_at_a_glance(astro_session_data[0].astro_hours)

    # moon summary block data
    summary_moon = summary_moon_data(astro_session_data[0].astro_hours)

    # top summary line for the next usable / best window
    next_good_night = get_next_good_astro(astro_session_data)

    # keep the full astro session list for the lookahead rows


    return {
        "go_no_go": go_no_go, 
        "at_a_glance": at_a_glance,
        "summary_moon" : summary_moon,
        "next_good_night" : next_good_night,
        "astro_session_data": astro_session_data,
    }


if __name__ == "__main__":
    # quick local check
    report = get_daily_report()
    print(report)