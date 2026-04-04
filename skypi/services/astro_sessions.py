"""
python -m skypi.services.astro_sessions
"""

from ..models import AstroSession
from ..utils.moon import get_moon_phase
from .forecaster import get_forecast


def best_astro_window(astro_date_hours):
    consec_hours_g = 0
    consec_g_hourlyforecast = []
    max_consec_g = 0
    max_consec_g_hourlyforecast = []

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

    best_astro_window = {
        "best_window_hours": max_consec_g_hourlyforecast,  # actual hours
        "best_window_length": max_consec_g,  # count of max
    }

    return best_astro_window


def astro_session_rating(best_astro_window):
    best_window_length = best_astro_window["best_window_length"]

    if best_window_length >= 3:
        gng = {"rag": "G", "result": "GO"}
    elif best_window_length == 2:
        gng = {"rag": "A", "result": "MAYBE"}
    else:
        gng = {"rag": "R", "result": "NO-GO"}

    return gng


def create_astro_sessions():
    forecast_hours = get_forecast()  # get forecast
    astro_date_list = []
    for hour in forecast_hours:
        if (  # skip blanks / already added
            hour.astro_date == None or hour.astro_date in astro_date_list
        ):
            pass

        else:
            astro_date_list.append(hour.astro_date)

    astro_session_data = []
    for date in astro_date_list:  # for each "astro" day

        astro_date_hours = []
        for hour in forecast_hours:  # run through all the hourlyforecasts
            if hour.astro_date == date:  # if the "astrodate" matches....
                astro_date_hours.append(hour)  # add to a list

        best_window_data = best_astro_window(astro_date_hours)  # best window in list

        astro_day = AstroSession(
            astro_date=date,
            astro_hours=astro_date_hours,
            astro_rating=astro_session_rating(best_window_data),
            astro_rating_window=best_window_data,
            astro_moon=get_moon_phase(astro_date_hours[0].moon_phase),
        )

        astro_session_data.append(astro_day)

    return astro_session_data


# print(astro_session_data[0])


def get_astro_sessions():
    # check cache
    # if cache more than 15mins old...
    # then get a new one
    # that checked (or done)... return the cached values
    astro_session_data = create_astro_sessions()
    return astro_session_data



def get_next_good_astro(astro_session_data):
    # first pass: look for G
    for session in astro_session_data:
        rag = session.astro_rating["rag"]
        if rag == "G":
            best_window = session.astro_rating_window
            hours = best_window["best_window_hours"]
            length = best_window["best_window_length"]

            if hours:
                start_time = hours[0].time.strftime("%H:%M")
                end_time = hours[-1].time.strftime("%H:%M")
            else:
                start_time = None
                end_time = None

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
            best_window = session.astro_rating_window
            hours = best_window["best_window_hours"]
            length = best_window["best_window_length"]

            if hours:
                start_time = hours[0].time.strftime("%H:%M")
                end_time = hours[-1].time.strftime("%H:%M")
            else:
                start_time = None
                end_time = None

            return {
                "next_good_night": session.astro_date,
                "next_good_night_rating": "A",
                "start_time": start_time,
                "end_time": end_time,
                "duration_hours": length,
            }

    # fallback: none found
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
