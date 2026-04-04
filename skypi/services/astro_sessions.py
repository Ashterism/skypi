"""
Builds the astro session view of the forecast.

Takes the hourly forecast data, groups it into astro nights,
works out the best continuous green window in each night,
and then gives each night an overall R/A/G rating.

Also provides the "next usable" / "best window" summary data
used in the UI.

Run directly with:
python -m skypi.services.astro_sessions
"""

from ..models import AstroSession
from ..utils.moon import get_moon_phase
from .forecaster import get_forecast


# Look through one astro night and find the longest continuous run of green hours.
# Returns both the actual hour objects in that run, and the length of the run.
def best_astro_window(astro_date_hours):
    # current green run we are in while looping through the hours
    consec_hours_g = 0
    consec_g_hourlyforecast = []
    # longest green run found so far
    max_consec_g = 0
    max_consec_g_hourlyforecast = []

    # step through the hours in this astro night and track green streaks
    for hour in astro_date_hours:
        if hour.overall_rating == "G":
            consec_hours_g += 1
            consec_g_hourlyforecast.append(hour)
            max_consec_g = max(max_consec_g, consec_hours_g)
            if max_consec_g == consec_hours_g:
                max_consec_g_hourlyforecast = consec_g_hourlyforecast

        else:
            consec_hours_g = 0
            consec_g_hourlyforecast = []

    # package up the best run we found
    best_astro_window = {
        "best_window_hours": max_consec_g_hourlyforecast,  # actual hours
        "best_window_length": max_consec_g,  # count of max
    }

    return best_astro_window


# Turn the best green window length into a simple night rating.
# 3+ green hours = good, 2 = maybe, otherwise no-go.
def astro_session_rating(best_astro_window):
    best_window_length = best_astro_window["best_window_length"]

    if best_window_length >= 3:
        gng = {"rag": "G", "result": "GO"}
    elif best_window_length == 2:
        gng = {"rag": "A", "result": "MAYBE"}
    else:
        gng = {"rag": "R", "result": "NO-GO"}

    return gng


# Build the full list of astro nights for the UI.
# Each astro session is one night with:
# - the hourly data for that night
# - the best green window in that night
# - the overall session rating
# - the moon phase icon for the row
def create_astro_sessions():
    forecast_hours = get_forecast()  # full hourly forecast with ratings already added
    # build a clean list of astro dates in order, without duplicates
    astro_date_list = []
    for hour in forecast_hours:
        if (  # skip blanks / already added
            hour.astro_date == None or hour.astro_date in astro_date_list
        ):
            pass

        else:
            astro_date_list.append(hour.astro_date)

    astro_session_data = []
    for date in astro_date_list:  # build one AstroSession per astro night

        astro_date_hours = []
        for hour in forecast_hours:  # pull out just the hours for this astro date
            if hour.astro_date == date:  # matching astro night
                astro_date_hours.append(hour)  # add hour to this night's list

        best_window_data = best_astro_window(astro_date_hours)  # longest green run in this night

        # package the night up into the dataclass used by the UI
        astro_day = AstroSession(
            astro_date=date,
            astro_hours=astro_date_hours,
            astro_rating=astro_session_rating(best_window_data),
            astro_rating_window=best_window_data,
            astro_moon=get_moon_phase(astro_date_hours[0].moon_phase),
        )

        astro_session_data.append(astro_day)

    return astro_session_data


# Handy for quick debugging if needed:
# print(astro_session_data[0])


# Main entry point for the rest of the app.
# Right now this just rebuilds everything each time.
# Later this is the obvious place to add caching.
def get_astro_sessions():
    # check cache
    # if cache more than 15mins old...
    # then get a new one
    # that checked (or done)... return the cached values
    astro_session_data = create_astro_sessions()
    return astro_session_data



# Find the next usable astro night for the top summary block.
# First look for the first green night.
# If there isn't one, fall back to the first amber night.
# Also returns the start/end time of that night's best green window.
def get_next_good_astro(astro_session_data):
    # first pass: look for G
    for session in astro_session_data:
        rag = session.astro_rating["rag"]
        if rag == "G":
            # pull out the best green window already worked out for this session
            best_window = session.astro_rating_window
            hours = best_window["best_window_hours"]
            length = best_window["best_window_length"]

            # if there is a best window, use the first and last hours as the time range
            if hours:
                start_time = hours[0].time.strftime("%H:%M")
                end_time = hours[-1].time.strftime("%H:%M")
            else:
                start_time = None
                end_time = None

            # return the first green session we find
            return {
                "next_good_night": session.astro_date,
                "next_good_night_rating": "G",
                "start_time": start_time,
                "end_time": end_time,
                "duration_hours": length,
            }

    # second pass: look for A
    for session in astro_session_data:
        rag = session.astro_rating["rag"]
        if rag == "A":
            # pull out the best green window already worked out for this session
            best_window = session.astro_rating_window
            hours = best_window["best_window_hours"]
            length = best_window["best_window_length"]

            # if there is a best window, use the first and last hours as the time range
            if hours:
                start_time = hours[0].time.strftime("%H:%M")
                end_time = hours[-1].time.strftime("%H:%M")
            else:
                start_time = None
                end_time = None

            # if no green session exists, return the first amber one instead
            return {
                "next_good_night": session.astro_date,
                "next_good_night_rating": "A",
                "start_time": start_time,
                "end_time": end_time,
                "duration_hours": length,
            }

    # if nothing usable found in the forecast horizon
    return {
        "next_good_night": None,
        "next_good_night_rating": None,
        "start_time": None,
        "end_time": None,
        "duration_hours": 0,
    }


if __name__ == "__main__":
    astro_session_data = create_astro_sessions()
    test = get_next_good_astro(astro_session_data)

    print(test)
    print("ran")
